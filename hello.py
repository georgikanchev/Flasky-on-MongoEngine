import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mongoengine import MongoEngine
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://127.0.0.1:10250/project1?ssl=true',
    'username': "localhost",
    'password': 'C2y6yDjf5' + r'/R' + '+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw' + r'/Jw=='
}


bootstrap = Bootstrap(app)
moment = Moment(app)
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


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.objects(username=form.name.data).first()
        role = Role.objects(name="user").first()
        if user is None:
            user = User(username=form.name.data, role_id=role)
            user.save()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


if __name__ == "__main__":
    app.run()
