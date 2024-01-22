from sqlalchemy import Column, ForeignKey, Integer, String, func, select
from sqlalchemy.orm import MapperProperty, column_property, relationship
from app.database import Base
from app.dish.models import Dish


class Submenu(Base):
    __tablename__ = 'submenus'
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), unique=True)
    description = Column(String(1000))
    menu_id: Column = Column(
        ForeignKey(
            'menus.id',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish',
        back_populates='submenus',
        cascade='all, delete',
        passive_deletes=True,
    )
    dishes_count: MapperProperty = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .correlate_except(Dish)
        .scalar_subquery(),
    )
