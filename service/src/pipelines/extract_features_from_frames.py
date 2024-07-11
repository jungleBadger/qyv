import os
import json
import torch
from torchvision import transforms
from PIL import Image
from transformers import SwinForImageClassification

class ExtractFeaturesFromFrames:
    def __init__(self, frames_dir: str):
        self.frames_dir = frames_dir
        self.output_dir = frames_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.model = SwinForImageClassification.from_pretrained("microsoft/swin-base-patch4-window7-224")
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def extract_features(self):
        frames = [f for f in os.listdir(self.frames_dir) if f.endswith('.jpg') or f.endswith('.png')]
        for frame in frames:
            features = self.process_frame(frame)
            self.save_features(frame, features)

    def process_frame(self, frame: str):
        frame_path = os.path.join(self.frames_dir, frame)
        image = Image.open(frame_path).convert("RGB")
        inputs = self.transform(image).unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            outputs = self.model(inputs)
            features = outputs.logits.squeeze().tolist()  # Convert tensor to list

        return features

    def save_features(self, frame: str, features: list):
        feature_data = {
            "frame": frame,
            "features": features
        }

        # Save features to JSON file
        json_path = os.path.join(self.output_dir, f"{os.path.splitext(frame)[0]}_features.json")
        with open(json_path, 'w') as json_file:
            json.dump(feature_data, json_file, indent=4)

        print(f"Processed and saved features for {frame}")

# Example usage
if __name__ == "__main__":
    frames_dir = "path_to_frames"
    extractor = ExtractFeaturesFromFrames(frames_dir)
    extractor.extract_features()
