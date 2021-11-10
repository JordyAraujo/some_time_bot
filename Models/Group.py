import peewee

from .BaseModel import BaseModel


class Group(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(max_length=255, unique=True)