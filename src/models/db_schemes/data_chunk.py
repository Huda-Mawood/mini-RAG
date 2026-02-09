from pydantic import BaseModel, Field
from typing import Optional

class DataChunk(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: str

    model_config = {
        "populate_by_name": True
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
