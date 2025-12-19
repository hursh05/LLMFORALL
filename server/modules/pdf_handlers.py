import os
import shutil
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploaded_docs")

def save_uploaded_files(files: list[UploadFile]) -> list[str]:
    """
    Saves uploaded PDF files to UPLOAD_DIR and returns their local paths.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_paths = []

    for file in files:
        save_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(save_path)

    return file_paths
