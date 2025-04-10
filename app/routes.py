# app/routes.py

from fastapi import APIRouter, UploadFile, File
from .analyze_image import analyze_image

router = APIRouter()


@router.post("/analyze")
async def analyze_image_and_get_moods(image: UploadFile = File(...)):
    contents = await image.read()
    top_moods = analyze_image(contents)
    return {"top_moods": top_moods}
