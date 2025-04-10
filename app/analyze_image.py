import torch
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
from .moods import MOOD_PROMPT_MAP

# Use GPU if available, otherwise fallback to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def analyze_image(file_bytes: bytes, top_k: int = 3):
    # Open the image from bytes and convert to RGB mode
    image = Image.open(BytesIO(file_bytes)).convert("RGB")

    # Extract mood names and corresponding prompts from MOOD_PROMPT_MAP
    moods = list(MOOD_PROMPT_MAP.keys())
    prompts = [" ".join(MOOD_PROMPT_MAP[mood]) for mood in moods]  # Concatenate mood prompts

    # Process the image and text prompts into inputs for the model
    inputs = processor(text=prompts, images=image, return_tensors="pt", padding=True, truncation=True).to(device)

    # Perform the forward pass and get the logits per image
    outputs = model(**inputs)

    # Logits for the image (how well the image matches each prompt)
    logits_per_image = outputs.logits_per_image

    # Apply softmax to get the probabilities (confidence of each mood)
    probs = logits_per_image.softmax(dim=1).detach().cpu().numpy()[0]

    # Sort the probabilities to get the top k moods
    top_indices = probs.argsort()[-top_k:][::-1]
    top_moods = [(moods[i], float(probs[i])) for i in top_indices]

    return top_moods
