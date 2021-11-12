import peewee
from peewee import ForeignKeyField

from .BaseModel import BaseModel
from .Group import Group
from .User import User


class Event(BaseModel):
    event_title = peewee.CharField(max_length=255, unique=True)
    event_group = ForeignKeyField(Group, backref='events', unique=True, null=True)
    event_user = ForeignKeyField(User, backref='events', unique=True, null=True)
    event_due = peewee.DateTimeField(formats='%Y-%m-%d %H:%M:%S')