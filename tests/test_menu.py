from sqlalchemy import select
from app.menu.models import Menu
from conftest import get_objects_list, menu_to_dict, get_object_id, get_object

router = '/api/v1/menus'
router_id = 'api/v1/menus/{id}'


# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка меню.
# 2. Создание меню. 
# 3. Вывод списка меню.
# 4. Получение меню по id.
# 5. Получение меню по несуществующему id. 
# 6. Изменеие меню
# 7. Удаление меню. 
# 8. Удаление меню по несуществующему id.

# pytest tests/test_menu.py -vv

async def test_get_empty_menu_list(ac, session):
    resp = await ac.get(router, follow_redirects=True)
    menu_list = await get_objects_list(Menu, session)
    assert resp.status_code == 200
    assert resp.json() == menu_list


async def test_create_menu(ac, session):
    resp = await ac.post(
        router,
        json={'title': 'My menu', 'description': 'My menu description'},
        follow_redirects=True
    )
    assert resp.status_code == 201
    menu_id = resp.json()["id"]
    menu = await session.get(Menu, menu_id)
    assert resp.json() == menu_to_dict(menu)


async def test_get_menu_list(ac, session):
    resp = await ac.get(router, follow_redirects=True)
    menu_list = await get_objects_list(Menu, session)
    assert resp.status_code == 200
    assert resp.json() == [menu_to_dict(menu) for menu in menu_list]


async def test_get_menu_by_id(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.get(
        router_id.format(id=menu_id),
    )
    menu = await get_object(Menu, session)
    assert resp.status_code == 200
    assert resp.json() == menu_to_dict(menu)


async def test_menu_not_found(ac):
    resp = await ac.get(
        router_id.format(id='8735869d-cd37-40b9-8148-b7d1c61d3723'),
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'menu not found'}


async def test_update_menu(ac, session):
    menu_id = await get_object_id(Menu, session)
    
    resp = await ac.patch(
        router_id.format(id=menu_id),
        json={
            'title': 'My updated menu',
            'description': 'My updated menu description',
        },
    )
    updated_menu = await get_object(Menu, session)

    assert resp.status_code == 200
    assert resp.json()['title'] == updated_menu.title
    assert resp.json()['description'] == updated_menu.description


async def test_delete_menu(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.delete(
        router_id.format(id=menu_id),
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'status': True,
        'message': 'The menu has been deleted',
     }


async def test_delete_menu_not_found(ac):
    resp = await ac.delete(
        router_id.format(id='8735869d-cd37-40b9-8148-b7d1c61d3723'),
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'menu not found'}


