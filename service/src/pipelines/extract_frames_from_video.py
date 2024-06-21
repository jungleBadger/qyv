import cv2
import os


class ExtractFramesFromVideo:
    def __init__(self, video_path: str, output_dir: str, fps: int):
        self.video_path = video_path
        self.output_dir = output_dir
        self.fps = fps

    def extract_frames(self):
        # Open the video file with OpenCV
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise Exception("Could not open video file")

        # Get video properties
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / video_fps

        # Calculate the interval for frame extraction
        frame_interval = int(video_fps / self.fps)

        frame_number = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_number % frame_interval == 0:
                frame_filename = os.path.join(self.output_dir, f"frame_{frame_number}.jpg")
                cv2.imwrite(frame_filename, frame)

            frame_number += 1

        cap.release()
