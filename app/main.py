from fastapi import FastAPI
from app.menu.router import router as router_menus


app = FastAPI()

app.include_router(router_menus)