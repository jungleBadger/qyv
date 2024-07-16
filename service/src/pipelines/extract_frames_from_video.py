import cv2
import os
import logging
import time


class ExtractFramesFromVideo:
    def __init__(self, video_path: str, output_dir: str, fps: int):
        self.video_path = video_path
        self.output_dir = output_dir
        self.fps = fps
        os.makedirs(output_dir, exist_ok=True)
        logging.basicConfig(level=logging.INFO)

    def extract_frames(self):
        # Open the video file with OpenCV
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise Exception("Could not open video file")

        # Get video properties
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / video_fps
        logging.info(f"Video FPS: {video_fps}, Total frames: {total_frames}, Duration: {duration:.2f} seconds")

        # Calculate the interval for frame extraction
        frame_interval = max(1, int(video_fps / self.fps))

        frame_number = 0
        extracted_frames = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_number % frame_interval == 0:
                frame_filename = os.path.join(self.output_dir, f"frame_{frame_number}.jpg")
                try:
                    cv2.imwrite(frame_filename, frame)
                    extracted_frames += 1
                    logging.info(f"Extracted frame {frame_number} to {frame_filename}")
                except Exception as e:
                    logging.error(f"Error saving frame {frame_number}: {e}")
                    time.sleep(0.1)  # Adding a small delay before retrying

            frame_number += 1

        cap.release()
        logging.info(f"Total extracted frames: {extracted_frames}")


# Example usage
if __name__ == "__main__":
    video_path = "path_to_video.mp4"
    output_dir = "output_frames"
    fps = 30  # Target FPS for frame extraction

    extractor = ExtractFramesFromVideo(video_path, output_dir, fps)
    extractor.extract_frames()
