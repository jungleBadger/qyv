from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import shutil
from src.pipelines.extract_frames_from_video import ExtractFramesFromVideo
from src.pipelines.handle_video_file import HandleVideoFile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

FRAMES_DIR = "frames"

# Ensure the frames directory exists
os.makedirs(FRAMES_DIR, exist_ok=True)


@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...), frames_per_second: int = Form(1)):
    # Create a subdirectory for this upload's frames
    logger.info("Received request to upload video")

    upload_id = file.filename.split('.')[0]
    upload_dir = os.path.join(FRAMES_DIR, upload_id)
    os.makedirs(upload_dir, exist_ok=True)

    handler = ""
    temp_video_path = ""
    try:
        # Handle the video file
        handler = HandleVideoFile(upload_dir=upload_dir)
        temp_video_path = handler.save_file(file)

        # Create an instance of the ExtractFramesFromVideo class
        extractor = ExtractFramesFromVideo(video_path=temp_video_path, output_dir=upload_dir, fps=frames_per_second)

        # Extract frames
        extractor.extract_frames()

        return JSONResponse(content={"message": "Frames extracted successfully", "frames_dir": upload_dir})

    except Exception as e:
        # Clean up in case of error
        logger.error(f"Error during processing: {str(e)}")

        shutil.rmtree(upload_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the uploaded video file
        if temp_video_path != "":
            handler.clean_up(temp_video_path)


@app.get("/")
def read_root():
    return {"Hello": "World"}
