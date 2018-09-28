from . import db


class Role(db.Document):
    name = db.StringField()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Document):
    username = db.StringField(max_length=50)
    role_id = db.ReferenceField(Role)

    def __repr__(self):
        return '<User %r>' % self.username

