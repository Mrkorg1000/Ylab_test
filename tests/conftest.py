import asyncio
from app.database import DATABASE_URL, Base
import pytest
from sqlalchemy import NullPool, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from httpx import AsyncClient
from main import app 
from app.config import settings
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish


DATABASE_URL_TEST = f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)

async_session_maker_test = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)
    

@pytest.fixture(autouse=True, scope='session') #(autouse=True, scope='session')
async def db() -> AsyncGenerator:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker_test() as db:
        try:
            yield db
        finally:
            await db.close()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    

    
@pytest.fixture 
async def session():
    async with async_session_maker_test() as session:
        yield session


@pytest.fixture
async def test_menu(session):
    menu = Menu(
        title = "My test menu",
        description = "Test menu description"
    )
    session.add(menu)
    await session.commit()
    await session.refresh(menu)
    return menu


@pytest.fixture
async def test_submenu(session, test_menu):
    submenu = Submenu(
        title="My test submenu",
        description="Test submenu description",
        menu_id = str(test_menu.id)
    )
    session.add(submenu)
    await session.commit()
    await session.refresh(submenu)
    return submenu


@pytest.fixture
async def test_dish(session, test_submenu):
    dish = Dish(
        title="My test dish",
        description="Test submenu dish",
        price = '99.99',
        submenu_id = str(test_submenu.id)
    )
    session.add(dish)
    await session.commit()
    await session.refresh(dish)
    return dish


def menu_to_dict(menu: Menu):
    return {
        'id': str(menu.id),
        'title': str(menu.title),
        'description': str(menu.description),
        'submenus_count': menu.submenus_count,
        'dishes_count': menu.dishes_count,
    }


def submenu_to_dict(submenu: Submenu):
    return {
        'id': str(submenu.id),
        'title': str(submenu.title),
        'description': str(submenu.description),
        'dishes_count': submenu.dishes_count,
    }


def dish_to_dict(dish: Dish):
    return {
        'id': str(dish.id),
        'title': str(dish.title),
        'description': str(dish.description),
        'price': str(dish.price),
    }


async def get_objects_list(obj_cls, session):
    query = select(obj_cls)
    result = await session.execute(query)
    objects_list = result.scalars().all()
    return objects_list


async def get_object(obj_cls, session):
    query = select(obj_cls)
    result = await session.execute(query)
    object = result.scalar_one_or_none()
    if object:
        return object

    

async def get_object_id(obj_cls, session):
    query = select(obj_cls)
    result = await session.execute(query)
    object = result.scalar_one_or_none()
    if object:
        return str(object.id)