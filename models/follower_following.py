from models.base_model import BaseModel
import peewee as pw
from models.user import User


class FollowerFollowing(BaseModel):
    fan = pw.ForeignKeyField(User, backref="idols")
    idol = pw.ForeignKeyField(User, backref="fans")
