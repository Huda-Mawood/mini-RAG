from abc import ABC, abstractmethod
from typing import List 
class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass 

    @abstractmethod 
    def is_collect_existed(self,collection_name:str)->bool:
        pass 

    @abstractmethod 
    def list_all_collections(self)->List:
        pass

    @abstractmethod
    def get_collection_info(self,collection_name:str)->dict:
        pass

    @abstractmethod 
    def delete_collection(self,collection_name:str):
        pass

    @abstractmethod 
    def create_collection(self,collection_name:str,
                          embedding_size:int,
                          do_reset:bool=False     # if the collection already exists, whether to reset it (delete all data and recreate it                   
                          ):
        pass 

    @abstractmethod 
    def insert_one(self,collection_name:str,text:str,vector:list,
                    metadata:dict=None,
                    record_id:str=None
                    ):
        pass

    @abstractmethod 
    def insert_many(self,collection_name:str,texts:list,
                    vectors:list,metadata:list=None,
                    record_ids:list=None,
                    batch_size:int=50 # batch insert to improve performance, default is 50, you can adjust it according to your needs   
                    ):
        pass 

    def search_by_vector(self,collection_name:str,
                         vector:list,
                         limit:int=5 # the number of results to return
                         
                         ):
        pass



        

