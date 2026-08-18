import shutil
from pathlib import Path
import chromadb

from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.schemas import QueryRequest, QueryResponse
from ingestion.ingest import ingest_document
from rag.rag_pipeline import (
    answer_question,
    refresh_rag_components
)


db_path = Path("chroma_db").resolve()

client = chromadb.PersistentClient(path=str(db_path))


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title = "RAG-API",
    description="Production-style RAG system",
    version = "1.0.0"
)



app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/query",response_model=QueryResponse)
def query(request: QueryRequest):

    result = answer_question(
        query = request.query
    )
    return QueryResponse(
    answer=result["answer"],
    sources=result["sources"]
)

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        client.delete_collection("general")
    except:
        pass

    collection = client.get_or_create_collection("general")

    result = ingest_document(
        str(file_path),
        collection
    )

    refresh_rag_components()

    return {
        "message": "Upload successful.",
        "filename": result["filename"],
        "chunks": result["chunks"]
    }

@app.delete("/collection")
def delete_collection():

    try:
        client.delete_collection("general")
    except Exception:
        return {
            "message": "Knowledge base is already empty."
        }

    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file():
            file_path.unlink()

    return {
        "message": "Knowledge base deleted successfully."
    }