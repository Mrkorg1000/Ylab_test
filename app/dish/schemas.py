from pydantic import UUID4, BaseModel


class SchemaDishBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SchemaDish(SchemaDishBase):
    id: UUID4
    price: str


class SchemaCreateUpdateDish(SchemaDishBase):
    price: str