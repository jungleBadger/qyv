import os
import shutil
from fastapi import UploadFile


class HandleVideoFile:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file: UploadFile) -> str:
        file_path = os.path.join(self.upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    def clean_up(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_file_path(self, filename: str) -> str:
        return os.path.join(self.upload_dir, filename)
