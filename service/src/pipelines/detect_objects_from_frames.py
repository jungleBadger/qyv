# src/pipelines/detect_objects_from_frames.py
import os
import json
import torch
from PIL import Image


class DetectObjectsFromFrames:
    def __init__(self, frames_dir: str):
        self.frames_dir = frames_dir
        self.output_dir = frames_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.model = torch.hub.load(
            'ultralytics/yolov5',
            'yolov5s',
            pretrained=True)  # Load YOLOv5 model

    def detect_objects(self):
        frames = [
            f for f in os.listdir(
                self.frames_dir) if f.endswith('.jpg') or f.endswith('.png')]
        for frame in frames:
            detections = self.process_frame(frame)
            self.save_detections(frame, detections)

    def process_frame(self, frame: str):
        frame_path = os.path.join(self.frames_dir, frame)
        image = Image.open(frame_path).convert("RGB")
        results = self.model(image)  # Perform object detection
        detections = results.pandas().xyxy[0].to_dict(
            orient="records")  # Convert detections to list of dictionaries
        return detections

    def save_detections(self, frame: str, detections: list):
        detection_data = {
            "frame": frame,
            "detections": detections
        }

        # Save detections to JSON file
        json_path = os.path.join(
            self.output_dir,
            f"{os.path.splitext(frame)[0]}_detections.json")
        with open(json_path, 'w') as json_file:
            json.dump(detection_data, json_file, indent=4)

        print(f"Processed and saved detections for {frame}")


# Example usage
if __name__ == "__main__":
    frames_dir = "path_to_frames"
    detector = DetectObjectsFromFrames(frames_dir)
    detector.detect_objects()
