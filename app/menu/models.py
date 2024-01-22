from sqlalchemy import Column, Integer, String, func, select
from sqlalchemy.orm import MapperProperty, column_property, relationship
from app.database import Base
from app.dish.models import Dish
from app.submenu.models import Submenu



class Menu(Base):
    __tablename__ = 'menus'
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), unique=True)
    description = Column(String(1000))
    submenus = relationship(
        'Submenu',
        back_populates='menu',
        cascade='all, delete',
        passive_deletes=True,
    )
    submenus_count: MapperProperty = column_property(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == id)
        .correlate_except(Submenu)
        .scalar_subquery(),
    )
    dishes_count: MapperProperty = column_property(
        select(func.count(Dish.id))
        .join(Submenu, Submenu.menu_id == id)
        .where(Dish.submenu_id == Submenu.id)
        .correlate_except(Submenu)
        .scalar_subquery(),
    )
