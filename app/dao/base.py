from fastapi import HTTPException, status
from app.database import async_session_maker
from sqlalchemy import select, insert
from fastapi.exceptions import ResponseValidationError
from app.menu.models import Menu
from app.menu.schemas import SchemaUpdateMenu


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        

    @classmethod
    async def update_object(cls, object_id: str, object_update_scheme):
        async with async_session_maker() as session:
            object_upd = await session.get(cls.model, object_id)
            if not object_upd:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="object not found"
                            )
            menu_data = object_update_scheme.dict(exclude_unset=True)
            for key, value in menu_data.items():
                setattr(object_upd, key, value)
            await session.commit()
            await session.refresh(object_upd)
            return object_upd


    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            object_list = result.scalars().all()
            # if object_list == []:
            #     return  { "detail": 'Not Found' } 
            # else:
            #     return object_list
            return object_list
    
    @classmethod
    async def add(cls, object):
        async with async_session_maker() as session:
            new_object = cls.model(**object.dict())
            session.add(new_object)
            await session.commit()
            await session.refresh(new_object)
            return new_object


    @classmethod
    async def delete(cls, object):
        async with async_session_maker() as session:
            await session.delete(object)
            await session.commit()
            