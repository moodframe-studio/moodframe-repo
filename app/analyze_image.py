import torch
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
from .moods import MOOD_PROMPT_MAP

# Detect GPU or CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Cache model and processor
model = None
processor = None

def get_model_and_processor():
    global model, processor
    if model is None or processor is None:
        model = CLIPModel.from_pretrained("laion/CLIP-ViT-B-32-laion2B-s34B-b79K").to(device)
        processor = CLIPProcessor.from_pretrained("laion/CLIP-ViT-B-32-laion2B-s34B-b79K")
    return model, processor

def analyze_image(file_bytes: bytes, top_k: int = 3):
    try:
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
    except UnidentifiedImageError:
        raise ValueError("Invalid image file. Please upload a valid image.")

    # Load lazily
    model, processor = get_model_and_processor()

    # Prepare moods
    moods = list(MOOD_PROMPT_MAP.keys())
    prompts = [" ".join(MOOD_PROMPT_MAP[mood]) for mood in moods]

    # Preprocess inputs
    inputs = processor(text=prompts, images=image, return_tensors="pt", padding=True, truncation=True).to(device)

    # Inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image

    # Softmax → top K moods
    probs = logits_per_image.softmax(dim=1).detach().cpu().numpy()[0]
    top_indices = probs.argsort()[-top_k:][::-1]
    top_moods = [(moods[i], float(probs[i])) for i in top_indices]

    return top_moods
