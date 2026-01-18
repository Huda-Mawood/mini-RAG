from pydantic import BaseModel, Field,validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    _id:Optional[ObjectId]
    project_id:str=Field(...,length=1)

    @validator('project_id')
    def validator_project_id(cls,value):
        if not value.isalnum():
            raise ValueError('project id must be alphanumeric')
        return value 
    
    class config:
        arbitrary_types_allowed=True    # to allow any type can't recognized by pydantic


