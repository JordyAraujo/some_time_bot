import peewee
from peewee import ForeignKeyField

from .BaseModel import BaseModel
from .Group import Group


class Event(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    title = peewee.CharField(max_length=255, unique=True)
    comment = peewee.CharField(max_length=255, unique=True)
    group = ForeignKeyField(Group, backref='events')
    datetime = peewee.DateTimeField(formats='%Y-%m-%d %H:%M:%S')