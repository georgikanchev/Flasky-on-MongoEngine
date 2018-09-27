from flask_mongoengine import MongoEngine
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://127.0.0.1:10250/project1?ssl=true',
    'username': "localhost",
    'password': 'C2y6yDjf5' + r'/R' + '+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw' + r'/Jw=='
}

db = MongoEngine()
db.init_app(app)


class Role(db.Document):
    name = db.StringField()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Document):
    username = db.StringField(max_length=50)
    role_id = db.ReferenceField(Role)

    def __repr__(self):
        return '<User %r>' % self.username


admin_role = Role(name="admin")
user_role = Role(name="user")
admin_role.save()
user_role.save()

user = User(username="Georgi", role_id=admin_role)
user.save()
