from  .BaseController import BaseController 
from models.db_schemes import Project,DataChunk, project
from stores.llm.LLMEnums import DocumentTypeEnums
from typing import List
import logging
import json 
class NLPController(BaseController):

    def __init__(self,vectordb_client,embedding_client,generation_client):
        super().__init__()

        self.vectordb_client=vectordb_client
        self.embedding_client=embedding_client
        self.generation_client=generation_client

    def create_collection_name(self,project_id: str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)

        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_vector_db_collection_info(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id)
        collection_info=self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info,default=lambda x: x.__dict__)
        ) 
    
    def index_into_vector_db(self,project:Project,chunks:List[DataChunk],
                             chunks_ids:List[int]
                             ,do_reset:bool=False):
        #step1: create collection name 
        collection_name=self.create_collection_name(project_id=project.project_id)

        #step2: manage items 
        texts=[c.chunk_text  for c in chunks]
        metadatas=[c.chunk_metadata  for c in chunks]
        # vectors=[
        #     self.embedding_client.embed_text(text=text,document_type=DocumentTypeEnums.DOCUMENT.value)
        #     for text in texts
        # ]
        vectors = self.embedding_client.embed_many(
                              texts=texts,
                              document_type=DocumentTypeEnums.DOCUMENT.value
                )

        #step3: create collection if not exist 
        _=self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset
        )

        #step4:insert into vector db
        _=self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadatas,
            vectors=vectors,
            record_ids=chunks_ids
        )

        return True
    def search_vector_db_collection(self,project:Project,text:str,limit:int=10):
        # step1: create collection name 
        collection_name=self.create_collection_name(project_id=project.project_id)

        # step2: get text embedding vector 
        vector=self.embedding_client.embed_text(
            text=text,
            document_type=DocumentTypeEnums.QUERY.value
        )
        if not vector:
            return False 
        
        # step3: do semantic search in vector db collection
        search_results=self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )
        if not search_results:
            return False
        return search_results


def answer_rag_question(self,project:Project,query:str,limit:10):

    #step 1:retriev related documents 
    retrieved_documents= self.search_vector_db_collection(
        project=project,
        text=query,
        limit=limit,
    )

    if not retrieved_documents or len(retrieved_documents)==0:
        return None 
    
    #step 2: Construct LLM prompt 

    system_prompt=""""
    
    """
        

