from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base



class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), unique=True)
    description = Column(String(1000))
    submenu_id: Column = Column(
        ForeignKey(
            'submenus.id',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    submenus = relationship('Submenu', back_populates='dishes')
    price = Column(String(50))