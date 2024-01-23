from app.dao.base import BaseDAO
from app.dish.models import Dish



class DishDAO(BaseDAO):
    model = Dish