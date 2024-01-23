from pydantic import UUID4, BaseModel


class SchemaSubmenuBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SchemaSubmenu(SchemaSubmenuBase):
    id: UUID4
    dishes_count: int


class SchemaCreateUpdateSubmenu(SchemaSubmenuBase):
    pass 