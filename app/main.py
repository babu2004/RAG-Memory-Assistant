from fastapi import FastAPI
from app.schemas import QueryRequest, QueryResponse
from rag.rag_pipeline import answer_question

app = FastAPI(
    title = "RAG-API",
    description="Production-style RAG system",
    version = "1.0.0"
)

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.get("/")
def root():
    return{
        "message":"welcome to the RAG API!"
    }

@app.post("/query",response_model=QueryResponse)
def query(request: QueryRequest):

    result = answer_question(
        query = request.query
    )
    return QueryResponse(
    answer=result["answer"],
    sources=result["sources"]
)

