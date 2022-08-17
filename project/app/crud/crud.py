from datetime import datetime

from core.db import database
from app.models.models import users, roles
from app.utils.crypt import crypt_pass

from app.schemas.schemas import UserBase
from asyncpg.exceptions import UniqueViolationError

from app.settings import logger


async def add_start_data_db():
    try:
        user = await database.fetch_one(users.select().where(users.c.login == 'admin'))
        if not user:
            user = users.insert().values(
                first_name='admin',
                last_name='admin',
                login='admin',
                hashed_password=crypt_pass('admin'),
                birthday=datetime.strptime('01-01-1970', '%d-%m-%Y')
            )
            user_id = await database.execute(user)
            role = roles.insert().values(user_id=user_id, role='Admin')
            await database.execute(role)
    except Exception as exc:
        logger.error(f'| Exception add start data to database: {exc}')


async def create(data: UserBase):
    try:
        hash_password = crypt_pass(data['password'])
        user = users.insert().values(
            first_name=data['first_name'],
            last_name=data['last_name'],
            login=data['login'],
            hashed_password=hash_password,
            birthday=datetime.strptime(data['birthday'], '%d-%m-%Y')
        )
        user_id = await database.execute(user)
        role = roles.insert().values(user_id=user_id, role='Read')
        await database.execute(role)
        return user_id
    except UniqueViolationError as exc:
        return str(exc.__dict__['detail'])
    except ValueError as exc:
        return str(exc)


async def get(user_id: int):
    try:
        user = dict(await database.fetch_one(users.select().where(users.c.id == user_id)))
        if user:
            return user
    except Exception as exc:
        logger.error(f'| Exception get function: {exc}')


async def delete(user_id: int):
    try:
        user = await database.fetch_one(users.select().where(users.c.id == user_id))
        if user:
            await database.fetch_one(roles.delete().where(roles.c.user_id == user_id))
            await database.fetch_one(users.delete().where(users.c.id == user_id))
            return True
        else:
            return False
    except Exception as exc:
        logger.error(f'| Exception delete function: {exc}')


async def update(user_id: int, data):
    try:
        user = await database.fetch_one(users.select().where(users.c.id == user_id))
        if user:
            await database.fetch_one(users.update().values(**data).where(users.c.id == user_id))
            return True
        else:
            return False
    except Exception as exc:
        logger.error(f'| Exception update function: {exc}')


async def get_role(user_id: int):
    try:
        role = await database.fetch_one(roles.select().where(roles.c.user_id == user_id))
        if role:
            return role.role
    except Exception as exc:
        logger.error(f'| Exception get_role function: {exc}')
