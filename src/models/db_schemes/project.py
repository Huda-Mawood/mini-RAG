from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from bson import ObjectId

class Project(BaseModel):
    id:Optional[ObjectId]= Field(default=None,alias="_id")
    project_id:str=Field(...,min_length=1)

    @field_validator('project_id')
    @classmethod
    def validator_project_id(cls,value):
        if not value.isalnum():
            raise ValueError('project id must be alphanumeric')
        return value 
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )   # to allow any type can't recognized by pydantic


