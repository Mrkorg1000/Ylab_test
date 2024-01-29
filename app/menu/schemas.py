from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict
from uuid import UUID

class SchemaMenuBase(BaseModel):
    title: str
    description: str

    class ConfigDict:
        orm_mode = True



class SchemaMenu(SchemaMenuBase):
    id: UUID
    submenus_count: int
    dishes_count: int

   

class SchemaCreateMenu(SchemaMenuBase):
    pass 

class SchemaUpdateMenu(SchemaMenuBase):
    pass 


