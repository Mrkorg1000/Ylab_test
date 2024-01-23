from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from sqlalchemy import select
from app.submenu.dao import SubmenuDAO
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.submenu.schemas import SchemaSubmenu, SchemaCreateUpdateSubmenu, SchemaSubmenuBase
from app.database import async_session_maker


router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=["Submenus"],
)


@router.get("", response_model=List[SchemaSubmenu])
async def get_submenus():
    submenus = await SubmenuDAO.find_all()
    return submenus


@router.get("/{id}", response_model=SchemaSubmenu)  
async def get_single_submenu(id: str):
    single_submenu = await SubmenuDAO.find_by_id(id)
    if not single_submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found"
                            )
    return single_submenu


@router.post("", response_model=SchemaSubmenu, status_code=status.HTTP_201_CREATED)
async def create_submenu(menu_id: str, submenu: SchemaCreateUpdateSubmenu):
    async with async_session_maker() as session:
        new_submenu = Submenu(
            title=submenu.title,
                description=submenu.description,
                menu_id=menu_id,
        )
        session.add(new_submenu)
        await session.commit()
        await session.refresh(new_submenu)
        return new_submenu
        


@router.delete("/{id}")
async def delete_single_submenu(id: str):
    submenu_to_delete = await SubmenuDAO.find_by_id(id)
    if not submenu_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="submenu not found"
                            )
    await SubmenuDAO.delete(submenu_to_delete)
    return {"status": True, "message": "The submenu has been deleted"}


@router.patch("/{id}", response_model=SchemaSubmenu)
async def update_submenu(id: str, submenu_scheme: SchemaCreateUpdateSubmenu):
    updated_submenu = await SubmenuDAO.update_object(id, submenu_scheme)  

    return updated_submenu
