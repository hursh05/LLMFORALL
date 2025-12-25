from fastapi import APIRouter, UploadFile, File
from server.modules.load_vectorstore import load_vectorstore
from pathlib import Path

router = APIRouter()

@router.post("/upload_pdfs/")
async def upload_pdfs(files: list[UploadFile] = File(...)):
    load_vectorstore(files)

    # IMPORTANT: return doc_id
    doc_id = Path(files[0].filename).stem

    return {
        "message": "Files uploaded successfully",
        "doc_id": doc_id
    }
