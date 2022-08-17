from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, text
from core.db import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
    Column("login", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("birthday", DateTime)
)

roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('role', String),
    Column('user_id', Integer, ForeignKey('users.id'))
)
