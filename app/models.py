from pydantic import BaseModel
from typing import List
from langchain.schema import Document

class QueryModel(BaseModel):
    question:str


class SearchResponse(BaseModel):
    ai_response:str
    similarity_search: List[Document]
    type: str
    message: str
    
class UploadResponse(BaseModel):
    type: str
    message: str

