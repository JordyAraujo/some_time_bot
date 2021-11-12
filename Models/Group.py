import peewee

from .BaseModel import BaseModel


class Group(BaseModel):
    group_id = peewee.CharField(max_length=30, unique=True)
    group_name = peewee.CharField(max_length=255, unique=True)