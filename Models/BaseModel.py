import peewee

from config import settings

db = peewee.SqliteDatabase('some_time_bot.db')

class BaseModel(peewee.Model):
    """Classe model base"""

    class Meta:
        database = db
