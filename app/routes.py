from fastapi import APIRouter, UploadFile, File, HTTPException
import asyncio
from app.analyze_image import analyze_image

router = APIRouter()


@router.post("/analyze_image")
async def analyze(file: UploadFile = File(...)):
    try:
        content = await file.read()

        # Run heavy computation in thread
        top_moods = await asyncio.to_thread(analyze_image, content)

        return {"top_moods": top_moods}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
