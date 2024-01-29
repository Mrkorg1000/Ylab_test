from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from uuid import UUID

from sqlalchemy import select
from app.dish.dao import DishDAO
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish
from app.dish.schemas import SchemaDish, SchemaCreateUpdateDish, SchemaDishBase
from app.database import async_session_maker
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"],
)


@router.get("", response_model=List[SchemaDish])
async def get_dishes():
    submenus = await DishDAO.find_all()
    return submenus


@router.get("/{id}", response_model=SchemaDish)  
async def get_single_dish(id: UUID):
    single_dish = await DishDAO.find_by_id(id)
    if not single_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found"
                            )
    return single_dish


@router.post("", response_model=SchemaDish, status_code=status.HTTP_201_CREATED)
async def create_dish(submenu_id: UUID, dish: SchemaCreateUpdateDish):
    async with async_session_maker() as session:
        new_dish = Dish(
            title=dish.title,
            description=dish.description,
            price=dish.price,
            submenu_id=submenu_id
        )
        session.add(new_dish)
        await session.commit()
        await session.refresh(new_dish)
        return new_dish
        


@router.delete("/{id}")
async def delete_single_dish(id: UUID):
    dish_to_delete = await DishDAO.find_by_id(id)
    if not dish_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="dish not found"
                            )
    await DishDAO.delete(dish_to_delete)
    return {"status": True, "message": "The dish has been deleted"}


@router.patch("/{id}", response_model=SchemaDish)
async def update_dish(id: UUID, dish_scheme: SchemaCreateUpdateDish):
    updated_dish = await DishDAO.update_object(id, dish_scheme)  

    return updated_dish
