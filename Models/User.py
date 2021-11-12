import peewee

from .BaseModel import BaseModel


class User(BaseModel):
    user_id = peewee.CharField(max_length=30, unique=True)
    user_username = peewee.CharField(max_length=255, unique=True)