from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property, hybrid_method


class FollowerFollowing(BaseModel):
    fan = pw.ForeignKeyField(User, backref="idols")
    idol = pw.ForeignKeyField(User, backref="fans")
    approved = pw.BooleanField(default=False)  # <<??? MIGHT CAUSE ISSUES

    @hybrid_method
    def is_following(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == user.id) & (FollowerFollowing.fan_id == self.id)) else False
