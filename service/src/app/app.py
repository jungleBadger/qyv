from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import shutil
from src.pipelines.extract_frames_from_video import ExtractFramesFromVideo
from src.pipelines.extract_features_from_frames import ExtractFeaturesFromFrames
from src.pipelines.extract_audio_and_transcribe_video import ExtractAudioAndTranscribeVideo
from src.pipelines.handle_video_file import HandleVideoFile
from src.pipelines.detect_objects_from_frames import DetectObjectsFromFrames
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

FRAMES_DIR = "frames"
AUDIO_DIR = "audio"
OUTPUT_DIR = "output"

# Ensure the frames directory exists
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...), frames_per_second: int = Form(1)):
    logger.info("Received request to upload video")

    upload_id = file.filename.split('.')[0]
    upload_frames_dir = os.path.join(FRAMES_DIR, upload_id)
    upload_audio_dir = os.path.join(AUDIO_DIR, upload_id)
    output_path = os.path.join(OUTPUT_DIR, f"{upload_id}_detected_objects.json")
    os.makedirs(upload_frames_dir, exist_ok=True)
    os.makedirs(upload_audio_dir, exist_ok=True)

    handler = ""
    temp_video_path = ""
    try:
        handler = HandleVideoFile(upload_dir=upload_frames_dir)
        temp_video_path = handler.save_file(file)

        extractor = ExtractFramesFromVideo(video_path=temp_video_path, output_dir=upload_frames_dir,
                                           fps=frames_per_second)
        extractor.extract_frames()

        transcriber = ExtractAudioAndTranscribeVideo(video_path=temp_video_path, output_dir=upload_audio_dir)
        transcript = transcriber.process()

        feature_extractor = ExtractFeaturesFromFrames(upload_frames_dir)
        feature_extractor.extract_features()

        object_detector = DetectObjectsFromFrames(upload_frames_dir)
        object_detector.detect_objects()

        return JSONResponse(content={"message": "Processing completed successfully", "output_path": output_path})

    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        shutil.rmtree(upload_frames_dir, ignore_errors=True)
        shutil.rmtree(upload_audio_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_video_path != "":
            handler.clean_up(temp_video_path)


@app.get("/")
def read_root():
    return {"Hello": "World"}
