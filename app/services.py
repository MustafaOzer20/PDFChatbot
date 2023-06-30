from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import PDFPlumberLoader
from langchain.schema import Document
from langchain.memory import ChatMessageHistory

from openai.embeddings_utils import get_embedding
from settings import OPENAI_API_KEY, VECTOR_STORE_PATH

from typing import List
import os
import openai


os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


class AI_Service:

    def build(self, texts: str, chunk_size:int=1000) -> None:
        """
        build function does; 
        1. split chunks
        2. clear db
        3. create embeddings
        4. init RetrievalQA

        :texts: pdf's text as str
        :chunk_size: length of chunks as int (default=1000)
        :return: None
        """
        self.texts = self.split_text_into_chunks(texts, chunk_size)
        self.clearDatabase(VECTOR_STORE_PATH)
        self.vectordb = self.create_embeddings(self.texts)
        self.rqa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=self.vectordb.as_retriever())
        self.history = ChatMessageHistory()
        

    @staticmethod
    def clearDatabase(path:str="persist") -> None:
        """
        clearDatabase function does old database clean.

        :path: database path as str
        :return: None
        """
        try:
            files = os.listdir(path=path)
        except FileNotFoundError:
            return
        
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                AI_Service.clearDatabase(file_path)   
    
    @staticmethod
    def split_text_into_chunks(texts: str, chunk_size:int=1000) -> List[str]:
        """
        split_text_into_chunks function does splits the text of the pdf into chunks.

        :path: database path as str
        :chunk_size: length of chunks as int (default=1000)
        :return: List[str]
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        texts = text_splitter.split_text(texts)
        return texts

    @staticmethod
    def create_embeddings(texts: List[str]) -> Chroma:
        """
        create_embeddings function does create vectorstore as Chroma.

        :texts: List of chunks(as str)
        :return: vectorstore as Chroma
        """
        embeddings = OpenAIEmbeddings()
        persist_directory = VECTOR_STORE_PATH
        if persist_directory not in os.listdir():
            os.mkdir(persist_directory)
        vectordb = Chroma.from_texts(texts, embeddings, persist_directory=persist_directory)
        Chroma.persist(vectordb)
        return vectordb

    @staticmethod
    def documents_join_question(documents:List[Document], question:str, k:int=2) -> str:
        """
        documents_join_question function does combines k documents with a question in a new text format.

        :documents: List of similarity document
        :question: client question as str
        :k: number of documents as int(default=2)
        :return: new question format as str
        """
        temp_documents = documents[:k]
        context = ""
        for doc in temp_documents:
            context += doc.page_content

        message = f"Aşağıda birkaç bilgi var:\n{context}\n\nVerilen bilgilere göre '{question}' sorusunun cevabı nedir?"

        return message    

    def ask(self, query: str, documents:List[Document], k:int=2) -> str:
        """
        ask function does;
        1. combines questions and similar documents
        2. asks the question to llm

        :query: client question as str
        :documents: List of similarity document
        :k: number of documents as int(default=2)
        :return: llm's answer as str
        """
        self.history.add_user_message(query)
        message = self.documents_join_question(documents, query, k=k)
        ai_response = self.rqa.run(message)
        self.history.add_ai_message(ai_response)
        #print(ai_response)
        return ai_response
    

def main():
    openai.api_key = OPENAI_API_KEY
    ai_service = AI_Service()

    ### Data
    texts = ""
    with open("app/test.txt", "r", encoding="utf-8") as f:
        texts+=f.read()

    ai_service.build(
        texts=texts
    )

    question = "Lojistik regresyon nedir?"

    query_vector = get_embedding(question, engine='text-embedding-ada-002')
    documents = ai_service.vectordb.similarity_search_by_vector(embedding=query_vector, k=4)
    response = ai_service.ask(question, documents)

    print(response)


if __name__ == "__main__":
    main()