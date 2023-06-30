import uvicorn
import io
import pdfplumber
import openai

from fastapi import FastAPI, UploadFile, HTTPException
from openai.embeddings_utils import get_embedding

from settings import OPENAI_API_KEY
from services import AI_Service
from models import QueryModel, SearchResponse, UploadResponse


app = FastAPI()
ai_service = AI_Service()
openai.api_key = OPENAI_API_KEY


@app.post("/upload")
async def file_upload(file: UploadFile) -> UploadResponse: # 
    if file.content_type != 'application/pdf':
        raise HTTPException(
            detail="Invalid file format. Only PDF files are supported.",
            status_code=400
        )

    file_data = await file.read()

    if len(file_data) == 0:
        raise HTTPException(
            detail="Empty file. Please upload a valid PDF file.",
            status_code=400
        )
    
    # pdf to text
    with io.BytesIO(file_data) as file_stream:
        pdf = pdfplumber.open(file_stream)
        texts = ""
        for page in pdf.pages:
            texts += page.extract_text()
        pdf.close()

    ai_service.build(texts, chunk_size=1000)

    return UploadResponse(
        type="message",
        message="Success!"
    )


@app.post("/search")
async def search(question:QueryModel) -> SearchResponse: # 
    try:
        query_vector = get_embedding(question.question,engine='text-embedding-ada-002')
        documents = ai_service.vectordb.similarity_search_by_vector(embedding=query_vector, k=4)
        response = ai_service.ask(query=question.question, documents=documents, k=2)
        return SearchResponse(
            ai_response= response,
            similarity_search = documents,
            type="success",
            message="Success!"
        )
    except (ValueError, AttributeError) as e:
        raise HTTPException(
            detail="File Upload Required!",
            status_code=400
        )




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)