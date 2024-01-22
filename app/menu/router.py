from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from sqlalchemy import select
from app.menu.dao import MenuDAO
from app.menu.models import Menu
from app.menu.schemas import SchemaMenu, SchemaCreateMenu, SchemaMenuBase, SchemaUpdateMenu
from app.database import async_session_maker
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/menus",
    tags=["Меню"],
)


@router.get("", response_model=List[SchemaMenu])
async def get_menus():
    return await MenuDAO.find_all()


@router.get("/{id}", response_model=SchemaMenu)  
async def get_single_menu(id: int):
    single_menu = await MenuDAO.find_by_id(id)
    if not single_menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
                            )
    return single_menu


@router.post("", response_model=SchemaMenu, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: SchemaCreateMenu):
    new_menu = await MenuDAO.add(menu)
    return new_menu


@router.delete("/{id}")
async def delete_single_menu(id: int):
    menu_to_delete = await MenuDAO.find_by_id(id)
    if not menu_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
                            )
    await MenuDAO.delete(menu_to_delete)
    return {"status": True, "message": "The menu has been deleted"}


@router.put("/{id}", response_model=SchemaMenu)
async def update_menu(id: int, menu_scheme: SchemaUpdateMenu):
    menu_to_update = await MenuDAO.find_by_id(id)  
    if not menu_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="menu not found"
                            )
    updated_menu = await MenuDAO.update_object(menu_to_update, menu_scheme)
    return updated_menu


    
    
    
    