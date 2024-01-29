from pydantic import UUID4, BaseModel
from uuid import UUID

class SchemaSubmenuBase(BaseModel):
    title: str
    description: str

    class ConfigDict:
        orm_mode = True


class SchemaSubmenu(SchemaSubmenuBase):
    id: UUID
    dishes_count: int


class SchemaCreateUpdateSubmenu(SchemaSubmenuBase):
    pass 