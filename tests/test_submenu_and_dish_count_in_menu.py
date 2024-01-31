from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish
from tests.conftest import get_object, get_object_id, get_objects_list, menu_to_dict, submenu_to_dict, dish_to_dict

router_menus = '/api/v1/menus'
router_menu_id = '/api/v1/menus/{id}'
router_submenus = '/api/v1/menus/{menu_id}/submenus'
router_submenu_id = '/api/v1/menus/{menu_id}/submenus/{id}'
router_dishes = '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'

# Проверка кол-ва блюд и подменю в меню

# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Создание меню. 
# 2. Создание подменю.
# 3. Создание блюда 1.
# 4. Создание блюда 2.
# 5. Просматриваем определенное меню
# 6. Просматриваем определенное подменю
# 7. Удаляет подменю
# 8. Вывод списка подменю.
# 9. Вывод списка блюд
# 10. Удаление меню.
# 11. Вывод списка меню.

# pytest tests/test_submenu_and_dish_count_in_menu.py -vv


async def test_create_menu(ac, session):
    resp = await ac.post(
        router_menus,
        json={'title': 'My menu', 'description': 'My menu description'},
        follow_redirects=True
    )
    assert resp.status_code == 201
    menu_id = resp.json()["id"]
    menu = await session.get(Menu, menu_id)
    assert resp.json() == menu_to_dict(menu)


async def test_create_submenu(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.post(
        router_submenus.format(menu_id=menu_id),
        json={'title': 'My submenu',
              'description': 'My submenu description',
              },
        follow_redirects=True    
    )
    assert resp.status_code == 201
    submenu_id = resp.json()["id"]
    submenu = await session.get(Submenu, submenu_id)
    assert resp.json() == submenu_to_dict(submenu)


async def test_create_dish_1(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.post(
        router_dishes.format(menu_id=menu_id, submenu_id=submenu_id),
        json={'title': 'My dish 1', 'description': 'My dish 1 description',
              'price': '12.50',
        },
        follow_redirects=True
    )
    assert resp.status_code == 201
    dish_id = resp.json()["id"]
    dish = await session.get(Dish, dish_id)
    assert resp.json() == dish_to_dict(dish)


async def test_create_dish_2(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.post(
        router_dishes.format(menu_id=menu_id, submenu_id=submenu_id),
        json={'title': 'My dish 2', 'description': 'My dish 2 description',
              'price': '99.50',
        },
        follow_redirects=True
    )
    assert resp.status_code == 201
    dish_id = resp.json()["id"]
    dish = await session.get(Dish, dish_id)
    assert resp.json() == dish_to_dict(dish)


async def test_get_menu_by_id(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.get(
        router_menu_id.format(id=menu_id),
    )
    menu = await get_object(Menu, session)
    assert resp.status_code == 200
    assert resp.json() == menu_to_dict(menu)
    


async def test_get_submenu_by_id(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.get(
        router_submenu_id.format(menu_id=menu_id, id=submenu_id)
    )
    submenu = await get_object(Submenu, session)
    assert resp.status_code == 200
    assert resp.json() == submenu_to_dict(submenu)


async def test_delete_submenu(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.delete(
        router_submenu_id.format(menu_id=menu_id, id=submenu_id)
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'status': True,
        'message': 'The submenu has been deleted',
    }


async def test_get_submenu_list(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.get(
        router_submenus.format(menu_id=menu_id),
        follow_redirects=True
    )
    submenu_list = await get_objects_list(Submenu, session)
    assert resp.status_code == 200
    assert resp.json() == [submenu_to_dict(submenu) for submenu in submenu_list]


async def test_get_dish_list(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.get(
        router_dishes.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            follow_redirects=True
        )
    )
    dish_list = await get_objects_list(Dish, session)
    assert resp.status_code == 200
    assert resp.json() == dish_list


async def test_delete_menu(ac, session):
    menu_id = await get_object_id(Menu, session)

    resp = await ac.delete(
        router_menu_id.format(id=menu_id),
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'status': True,
        'message': 'The menu has been deleted',
     }


async def test_get_menu_list(ac, session):
    resp = await ac.get(router_menus, follow_redirects=True)
    menu_list = await get_objects_list(Menu, session)
    assert resp.status_code == 200
    assert resp.json() == menu_list
