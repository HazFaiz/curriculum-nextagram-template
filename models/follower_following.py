from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property, hybrid_method


class FollowerFollowing(BaseModel):
    fan = pw.ForeignKeyField(User, backref="idols")  # ppl im trying foolow
    idol = pw.ForeignKeyField(User, backref="fans")  # ppl trying to folow me
    approved = pw.BooleanField(default=False)  # <<??? MIGHT CAUSE ISSUES
