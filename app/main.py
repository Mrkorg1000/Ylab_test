from fastapi import FastAPI
from app.menu.router import router as router_menus
from app.submenu.router import router as router_submenus
from app.dish.router import router as router_dish


app = FastAPI()

app.include_router(router_menus)
app.include_router(router_submenus)
app.include_router(router_dish)