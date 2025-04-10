import torch
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
from .moods import MOOD_PROMPT_MAP

device = "cuda" if torch.cuda.is_available() else "cpu"

def analyze_image(file_bytes: bytes, top_k: int = 3):
    try:
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
    except UnidentifiedImageError:
        raise ValueError("Invalid image file. Please upload a valid image.")

    # Lazy-load the model and processor here to reduce startup RAM
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    moods = list(MOOD_PROMPT_MAP.keys())
    prompts = [" ".join(MOOD_PROMPT_MAP[mood]) for mood in moods]

    inputs = processor(text=prompts, images=image, return_tensors="pt", padding=True, truncation=True).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image

    probs = logits_per_image.softmax(dim=1).detach().cpu().numpy()[0]

    top_indices = probs.argsort()[-top_k:][::-1]
    top_moods = [(moods[i], float(probs[i])) for i in top_indices]

    return top_moods
