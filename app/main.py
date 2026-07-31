from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.schemas import QueryRequest, QueryResponse
from rag.rag_pipeline import answer_question



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

