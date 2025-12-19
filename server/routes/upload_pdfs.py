from fastapi import APIRouter, UploadFile, File
from modules.load_vectorstore import load_vectorstore

router = APIRouter()

@router.post("/upload_pdfs/")
async def upload_pdfs(files: list[UploadFile] = File(...)):
    load_vectorstore(files)
    return {"message": "Files uploaded successfully"}
