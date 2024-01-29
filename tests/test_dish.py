from app.dish.models import Dish
from app.menu.models import Menu
from app.submenu.models import Submenu
from tests.conftest import dish_to_dict, get_object_id


router = '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
router_id = 'api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{id}'

# pytest tests/test_dish.py -vv

# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка блюд.
# 2. Создание блюда.
# 3. Вывод списка блюд.
# 4. Получение блюда по id.
# 5. Получение блюда по несуществующему id.
# 6. Изменеие блюда
# 7. Удаление блюда.
# 8. Удаление блюда по несуществующему id.


async def test_get_empty_dish_list(ac, test_submenu):
    resp = await ac.get(
        router.format(menu_id=str(test_submenu.menu_id),
        submenu_id=str(test_submenu.id)),
        follow_redirects=True
    )
    assert resp.status_code == 200
    assert resp.json() == []


async def test_create_dish(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.post(
        router.format(menu_id=menu_id, submenu_id=submenu_id),
        json={'title': 'My super dish', 'description': 'My super dish description',
              'price': '12.50',
        },
        follow_redirects=True
    )
    assert resp.status_code == 201
    dish_id = resp.json()["id"]
    dish = await session.get(Dish, dish_id)
    assert resp.json() == dish_to_dict(dish)


async def test_get_dish_list(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)
    dish_id = await get_object_id(Dish, session)

    resp = await ac.get(
        router.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            follow_redirects=True
        )
    )
    assert resp.status_code == 200
    assert resp.json() == [
        {
        'title': 'My super dish',
        'description': 'My super dish description',
        'id': dish_id,
        'price': '12.50',
        }
    ]


async def test_get_dish_by_id(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)
    dish_id = await get_object_id(Dish, session)

    resp = await ac.get(
        router_id.format(menu_id=menu_id, submenu_id=submenu_id,
        id=dish_id)
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'title': 'My super dish',
        'description': 'My super dish description',
        'id': dish_id,
        'price': '12.50',
        }


async def test_dish_not_found(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)
    
    resp = await ac.get(
        router_id.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id='8735869d-cd37-40b9-8148-b7d1c61d3723'
        )
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'dish not found'}


async def test_update_dish(ac, session):
     menu_id = await get_object_id(Menu, session)
     submenu_id = await get_object_id(Submenu, session)
     dish_id = await get_object_id(Dish, session)

     resp = await ac.patch(
        router_id.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish_id
        ),
        json={
            'title': 'My updated dish',
            'description': 'My updated dish description',
            'price': '14.50',
        },
    )
     assert resp.status_code == 200
     assert resp.json() == {
        'title': 'My updated dish',
        'description': 'My updated dish description',
        'id': dish_id,
        'price': '14.50',
    }


async def test_delete_dish(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)
    dish_id = await get_object_id(Dish, session)

    resp = await ac.delete(
        router_id.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id=dish_id
        )
    )
    assert resp.status_code == 200
    assert resp.json() == {
        'status': True,
        'message': 'The dish has been deleted',
    }


async def test_delete_dish_not_found(ac, session):
    menu_id = await get_object_id(Menu, session)
    submenu_id = await get_object_id(Submenu, session)

    resp = await ac.delete(
        router_id.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            id='8735869d-cd37-40b9-8148-b7d1c61d3723'),
    )
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'dish not found'}