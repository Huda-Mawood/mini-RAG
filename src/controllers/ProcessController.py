from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader 
from models import ProcessingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)
   
    def get_file_extension(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self,file_id:str):
        file_extension=self.get_file_extension(file_id=file_id)
        file_path=os.path.join(
            self.project_path,
            file_id
        )
        if file_extension==ProcessingEnum.TXT.value:
            return TextLoader(file_path,encoding='utf-8')
        if file_extension==ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None
    
    def get_file_content(self,file_id:str):
        loader=self.get_file_loader(file_id=file_id)
        return loader.load()
    
    def process_file_content(self,file_content:list,file_id:str,chunk_size:int=100,chunk_overlap:int=20):
        txt_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,

        )

        # file_content_texts=[
        #     rec.page_content
        #     for rec in file_content
        # ]
        # file_content_metadata=[
        #     rec.metadata
        #     for rec in file_content
        # ]

        chunks=txt_splitter.split_documents(
            file_content
        )

        return chunks



