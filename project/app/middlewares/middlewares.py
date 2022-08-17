import sys
import jwt

from aiohttp import web
from app.utils.jwt import JWT_SECRET, JWT_ALGORITHM
from core.db import database
from app.models.models import users
from app.crud.crud import get_role

from app.settings import logger
# from loguru import logger
# # Logger
# logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
# logger.add("logs/file_1.log", rotation="500 MB")


async def auth_middleware(_, handler):
    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('Authorization', None)

        user_agent = request.headers['User-Agent']
        ip_addr = request.remote
        req_method = request.method
        req_path = request.path

        logger.info(
            "| Login request: "
            f"USER-AGENT: {user_agent}, "
            f"IP: {ip_addr}, "
            f"METHOD: {req_method}, "
            f"PATH: {req_path}, "
            f"JWT-TOKEN: {jwt_token}"
        )
        if request.path == '/login':
            # Logs login request
            return await handler(request)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET,
                                     algorithms=[JWT_ALGORITHM])

                user_id = payload['user_id']
                # Logs authorization users

                # Get user role
                role = await get_role(user_id)

                if role == 'Block':
                    return web.json_response({'message': 'You are blocked'}, status=403)

                # Checking for admin
                if (request.method in ['POST', 'PUT', 'DELETE']) and (not role == 'Admin'):
                    return web.json_response({'message': 'You don\'t have enough rights'}, status=403)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return web.json_response({'message': 'Token is invalid'}, status=400)

            request.user = await database.fetch_one(users.select().where(users.c.id == user_id))
        else:
            # logger.info(
            #     "| Don't have enough rights: "
            #     f"USER-AGENT: {user_agent}, "
            #     f"IP: {ip_addr}, "
            #     f"METHOD: {req_method}, "
            #     f"PATH: {req_path}, "
            #     f"JWT-TOKEN: {jwt_token}"
            # )
            return web.json_response({'message': 'You don\'t have enough rights'}, status=403)
        return await handler(request)
    return middleware
