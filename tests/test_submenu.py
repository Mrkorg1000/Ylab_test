from app.menu.models import Menu
from app.submenu.models import Submenu
from tests.conftest import get_object_id, submenu_to_dict


router = '/api/v1/menus/{menu_id}/submenus'
router_id = 'api/v1/menus/{menu_id}/submenus/{id}'


# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка подменю. 
# 2. Создание подменю.
# 3. Вывод списка подменю.
# 4. Получение подменю по id.
# 5. Получение подменю по несуществующему id.
# 6. Изменение подменю
# 7. Удаление подменю.
# 8. Удаление меню по несуществующему id.

# pytest tests/test_submenu.py -vv


async def test_get_empty_submenu_list(ac, test_menu):
    resp = await ac.get(
        router.format(menu_id=str(test_menu.id)),
        follow_redirects=True                   
    )
    assert resp.status_code == 200
    assert resp.json() == []


async def test_create_submenu(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.post(
        router.format(menu_id=menu_id),
        json={'title': 'My submenu',
              'description': 'My submenu description',
              },
        follow_redirects=True    
    )
    assert resp.status_code == 201
    submenu_id = resp.json()["id"]
    submenu = await session.get(Submenu, submenu_id)
    assert resp.json() == submenu_to_dict(submenu)


async def test_get_submenu_list(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.get(
        router.format(menu_id=menu_id),
        follow_redirects=True
    )
    assert resp.status_code == 200
    assert resp.json() == [
        {
        'title': 'My submenu',
        'description': 'My submenu description',
        'id': submenu_id,
        'dishes_count': 0,
        }
    ]


async def test_get_submenu_by_id(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.get(
        router_id.format(menu_id=menu_id, id=submenu_id)
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'title': 'My submenu',
        'description': 'My submenu description',
        'id': submenu_id,
        'dishes_count': 0,
    }


async def test_submenu_not_found(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.get(
        router_id.format(menu_id=menu_id, id='8735869d-cd37-40b9-8148-b7d1c61d3723'),
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'submenu not found'}


async def test_update_submenu(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.patch(
        router_id.format(menu_id=menu_id, id=submenu_id),
        json={
            'title': 'My updated submenu',
            'description': 'My updated submenu description',
        },
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'title': 'My updated submenu',
        'description': 'My updated submenu description',
        'id': submenu_id,
        'dishes_count': 0,
    }


async def test_delete_submenu(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.delete(
        router_id.format(menu_id=menu_id, id=submenu_id)
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'status': True,
        'message': 'The submenu has been deleted',
    }


async def test_delete_submenu_not_found(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.delete(
        router_id.format(menu_id=menu_id, id='8735869d-cd37-40b9-8148-b7d1c61d3723'),
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'submenu not found'}

