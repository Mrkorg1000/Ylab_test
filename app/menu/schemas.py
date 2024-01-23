from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict


class SchemaMenuBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True



class SchemaMenu(SchemaMenuBase):
    id: UUID4
    submenus_count: int
    dishes_count: int

   

class SchemaCreateMenu(SchemaMenuBase):
    pass 

class SchemaUpdateMenu(SchemaMenuBase):
    pass 


