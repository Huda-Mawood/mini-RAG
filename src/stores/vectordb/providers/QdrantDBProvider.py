from qdrant_client import QdrantClient,models
from ..VectorDBInterface import VectorDBInterface 
from ..VectorDBEnums import DistantMethodEnums
from typing import List 
import logging 
from models.db_schemes import ReterievedDocument

class QdrantDBProvider(VectorDBInterface):
    def __init__(self,db_path:str,
                 distance_method:str):
        
        self.client=None # i will initialize in connect method 
        self.db_path=db_path 
        self.distance_method=None  

        if distance_method == DistantMethodEnums.COSINE.value:
            self.distance_method=models.Distance.COSINE

        elif distance_method==DistantMethodEnums.DOT.value:
            self.distance_method=models.Distance.DOT 

        else:
            self.distance_method = models.Distance.COSINE # default distance method is cosine

        self.logger=logging.getLogger(__name__)

    def connect(self):
        self.client=QdrantClient(path=self.db_path)
    
    def disconnect(self):
        self.client=None

    def is_collect_existed(self,collection_name:str)->bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self)->List:
        return self.client.get_collection()
    
    def get_collection_info(self,collection_name:str)->dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self,collection_name:str):
        if self.is_collect_existed(collection_name):
             return self.client.delete_collection(collection_name=collection_name)
        
    def create_collection(self,collection_name:str,
                          embedding_size:int,
                          do_reset:bool=False     # if the collection already exists, whether to reset it (delete all data and recreate it                   
                          ):
        if do_reset: # if the collection already exists and do_reset is True, then delete the collection and recreate it
            _=self.delete_collection(collection_name=collection_name)  #_= is variable to receive the return value of delete_collection, but we don't care about it, so we use _ to indicate that we don't care about it

        if not self.is_collect_existed(collection_name=collection_name):
            _=self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )
            return True 
        
        return False 
    
    def insert_one(self,collection_name:str,text:str,vector:list,
                    metadata:dict=None,
                    record_id:str=None
                    ):
        if not self.is_collect_existed(collection_name=collection_name):
             self.logger.error(f"Collection {collection_name} does not exist, please create it first")
             return False 
         
        try:
            _=self.client.upsert(
                    collection_name=collection_name,
                    points=[
                        
                        models.PointStruct(
                            id=[record_id] if record_id else None,
                            vector=vector,
                            payload={  # the payload is the metadata of the record, you can store any information you want in the payload, such as the original text, the source of the data, etc. In this case, we store the original text in the payload with the key "text" and metadata in the payload with the key "metadata"
                                "text":text,
                                "metadata":metadata
                            }
                        )
                    ]    
                )
        except Exception as e :
            self.logger.error(f"Failed to insert record into collection {collection_name}, error: {e}")
            return False
        
        return True

    def insert_many(self,collection_name:str,texts:list,
                    vectors:list,metadata:list=None,
                    record_ids:list=None,
                    batch_size:int=50 # batch insert to improve performance, default is 50, you can adjust it according to your needs   
                    ):
        if metadata is None:
            metadata=[None]*len(texts)

        if record_ids is None:
            record_ids=list(range(0,len(texts)))

        
        for i in range(0, len(texts), batch_size):
            batch_end=i+batch_size
            batch_texts=texts[i:batch_end]
            batch_vectors=vectors[i:batch_end]
            batch_metadata=metadata[i:batch_end]
            batch_record_ids=record_ids[i:batch_end]

            batch_points =[

                models.PointStruct(
                    id=batch_record_ids[x] if batch_record_ids[x] is not None else x,
                    vector=batch_vectors[x],
                    payload={
                        "text":batch_texts[x],
                        "metadata":batch_metadata[x]
                    }
                )
                
                for x in range(len(batch_texts))
            ]
            try:
                _=self.client.upsert(
                    collection_name=collection_name,
                    points=batch_points
                )
            except Exception as e:
                self.logger.error(f"Failed to insert batch records into collection {collection_name}, error: {e}")
                return False

        return True
    
    def search_by_vector(self,collection_name:str,
                         vector:list,
                         limit:int=5 # the number of results to return
                         
                         ):
        results= self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit
        ).points

        if not results or len(results)==0:
            return None
        
        return [
            ReterievedDocument(**{
                "score":result.score,
                "text":result.payload["text"]
            })

            for result in results
        ]
    





        

       
    
