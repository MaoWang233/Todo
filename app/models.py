from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String)
    done = db.Column(db.Boolean)

    def from_json(self, source):
        if 'title' in source:
            self.title = source['title']
        if 'done' in source:
            self.done = source['done']

    def to_json(self):
        return {"id": self.id,
                "title": self.title,
                "done": self.done}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
