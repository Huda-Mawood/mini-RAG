from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: str
    chunk_asset_id:str
    
    @field_validator("id", mode="before")  # ✅ حول ObjectId لـ string
    @classmethod
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = {
           "populate_by_name": True,
           "arbitrary_types_allowed": True
    }

    @classmethod
    def get_indexes(cls):
        return[
            {
                'key':[('chunk_project_id',1)],
                'name':'chunk_project_id_index_1',
                'unique':False  # because multiple chunks can belong to the same project
            }
        ]
    
class ReterievedDocument(BaseModel):
    text:str
    score:float
