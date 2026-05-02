from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id:Optional[ObjectId]=Field(None,alias="_id")
    asset_project_id:ObjectId
    asset_type:str=Field(...,min_length=1)
    asset_name:str=Field(...,min_length=1)
    asset_size:int=Field(gt=0,default=None)
    asset_config:dict=Field(default=None)
    asset_pushed_at:datetime=Field(default=datetime.utcnow())

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )   # to allow any type can't recognized by pydantic

    @classmethod
    def get_indexes(cls):
        return[
            {
                'key':[('asset_project_id',1)],
                'name':'asset_project_id_index_1',
                'unique':False
            },
            {
                'key':[('asset_project_id',1),
                       ('asset_name',1)
                       ],
                'name':'asset_project_id_asset_name_index_1',
                'unique':True # to ensure that asset name is unique within the same project
            }
        ]

