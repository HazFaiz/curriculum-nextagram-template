from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property, hybrid_method
import re


class User(BaseModel):
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=False)
    profile_image = pw.CharField(null=True)
    private = pw.BooleanField(default=True)

    @hybrid_property
    def profile_image_url(self):
        # if changed provider, just need to change the url
        if self.profile_image:
            return f"https://nextacademyhf.s3-ap-southeast-1.amazonaws.com/{self.profile_image}"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def validate(self):
        # pattern = "[A-Za-z0-9@#$%^&+=]"
        # ------------------- CHECK FOR VALID PASSWORD -------------

        # ------ CHECK FOR EXISTING NAME ----
        #  IF the existing_username exists AND the existing id NOT the same as self.id
        existing_username = User.get_or_none(User.name == self.name)
        if existing_username and not existing_username.id == self.id:
            self.errors.append('Username already taken')

        # ------ CHECK FOR EXISTING EMAIL ----
        existing_email = User.get_or_none(User.email == self.email)
        if existing_email and not existing_email.id == self.id:
            self.errors.append('Account with this email already exists')

        if not self.id:
            regexcheck = re.match(
                r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{6,}$', self.password)
            if len(self.password) <= 6:
                self.errors.append('Password must be more than 6 characters')
            elif not (regexcheck):
                self.errors.append(
                    'Password must have atleast the following: one uppercase letter, one lowercase letter, and one special character')
            else:
                self.password = generate_password_hash(self.password)

        return True

# ----- DETERMINES IF FOLLOWING AN IDOL OR NOT --------------

    @hybrid_method
    def is_following(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == user.id) & (FollowerFollowing.fan_id == self.id)) else False

# ------ PRIVATE PROFILE PROPERTY ---------------

    @hybrid_property
    def is_private(self):
        if self.private:
            return True
        else:
            return False

# ------ SANDRA HELPED WITH BELOW LOGIC. GIVE HER FOOD -----

    @hybrid_method
    def is_approved(self, user, current_user):
        from models.follower_following import FollowerFollowing
        user = FollowerFollowing.get_or_none(
            FollowerFollowing.idol_id == user.id)
        current_user = FollowerFollowing.get_or_none(
            FollowerFollowing.fan_id == self.id)
        if user and current_user.approved == True:
            return True
        return False

        # return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == user.id) & (FollowerFollowing.fan_id == self.id) & (yourself.approved == True) else False
