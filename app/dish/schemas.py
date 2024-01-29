from pydantic import UUID4, BaseModel
from uuid import UUID

class SchemaDishBase(BaseModel):
    title: str
    description: str

    class ConfigDict:
        orm_mode = True


class SchemaDish(SchemaDishBase):
    id: UUID
    price: str


class SchemaCreateUpdateDish(SchemaDishBase):
    price: str