import json
from aiohttp import web

from core.db import database
from app.models.models import users, roles
from app.crud.crud import create, get, delete, update, add_start_data_db
from app.utils.crypt import check_pass
from app.utils.jwt import get_token


routes = web.RouteTableDef()


async def on_startup(app):
    print('on_startup')
    await database.connect()
    await add_start_data_db()


async def on_shutdown(app):
    print('on_shutdown')
    await database.disconnect()


@routes.post('/login')
async def login(request):
    data = await request.post()
    user = await database.fetch_one(users.select().where(users.c.login == data['login']))
    if user:
        if check_pass(data['password'], user.hashed_password):
            jwt_token = await get_token(user.id)
            return web.json_response({'token': jwt_token})
        else:
            return web.json_response({'message': 'Wrong credentials'}, status=400)
    else:
        return web.json_response({'message': 'Wrong credentials'}, status=400)


@routes.post('/users/create')
async def create_user(request):
    """
    Create user
    :return: json response
    """
    data = await request.post()
    result = await create(data)
    if isinstance(result, int):
        return web.json_response(
            {
                'status': 'success',
                'message': 'User created successfully'
            }, status=201
        )
    else:
        return web.json_response(
            {
                'status': 'error',
                'message': result
            }, status=400
        )


@routes.get('/users/all')
async def get_users(request):
    """
    Get All Users from database
    :return: json response
    """
    results = await database.fetch_all(users.select().limit(10))
    users_list = [dict(result) for result in results]
    for user in users_list:
        user['birthday'] = str(user['birthday'])

    web.Response(text=json.dumps(users_list))
    return web.json_response(
        {
            'status': 'success',
            'users': users_list
        }, status=200
    )


@routes.get('/users/{user_id}')
async def get_user(request):
    user_id = int(request.match_info["user_id"])
    user = await get(user_id)
    if user:
        return web.json_response(
            {
                'status': 'success',
                'user': {
                    'id': user['id'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'login': user['login'],
                    'hashed_password': user['hashed_password'],
                    'birthday': str(user['birthday']),
                }
            }, status=200
        )
    else:
        return web.json_response(
            {
                'status': 'error',
                'message': 'User does not exist'
            }, status=400
        )


@routes.delete('/users/{user_id}')
async def delete_user(request):
    user_id = int(request.match_info["user_id"])
    res = await delete(user_id)
    if res:
        return web.json_response(
            {
                'status': 'success',
                'message': 'User deleted successfully'
            }, status=200
        )
    else:
        return web.json_response(
            {
                'status': 'error',
                'message': 'User does not exist'
            }, status=400
        )


@routes.put('/users/{user_id}')
async def update_user(request):
    data = await request.post()
    user_id = int(request.match_info["user_id"])
    res = await update(user_id, data)
    if res:
        return web.json_response(
            {
                'status': 'success',
                'message': 'User update successfully'
            }, status=200
        )
    else:
        return web.json_response(
            {
                'status': 'error',
                'message': 'User does not exist'
            }, status=400
        )
