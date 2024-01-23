from sqlalchemy import Column, Float, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
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
    price = Column(String, nullable=False)