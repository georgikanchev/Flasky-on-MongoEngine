from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from mongoengine import *
from mongoengine import signals
from . import db, login_manager
from bson.objectid import ObjectId


class Role(db.Document):
    name = db.StringField()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Document, UserMixin):

    username = db.StringField(max_length=50)
    email = db.StringField()
    role_id = db.ReferenceField(Role)
    password = db.StringField()
    password_hashed = db.BooleanField(default=False)

    def clean(self):
        if not self.password_hashed:
            self.password = generate_password_hash(self.password)
            self.password_hashed = True

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.objects(_id=ObjectId(user_id))
