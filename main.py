from fastapi import FastAPI
from app.database import Base, engine
from app.config import settings
from app.menu.router import router as router_menus
from app.submenu.router import router as router_submenus
from app.dish.router import router as router_dish


app = FastAPI()

app.include_router(router_menus)
app.include_router(router_submenus)
app.include_router(router_dish)

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


