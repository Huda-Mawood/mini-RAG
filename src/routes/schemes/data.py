from pydantic import BaseModel
from typing import Optional
#this name to know this is class specific endpoint requests
class ProcessRequest(BaseModel):
    file_id:str
    chunk_size:Optional[int]=100
    overlap_size:Optional[int]=20
    do_reset:Optional[int]=0
