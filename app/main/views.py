from flask import render_template, redirect, request, url_for, flash, jsonify, json
from flask.ext.login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Todo
from . import main
from ..note import note
from .forms import LoginForm, RegistrationForm


@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('note.todo'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/todo', methods=['POST'])
def create():
    todo = Todo()
    todo.from_json(request.get_json())
    todo.user_id = current_user.id
    db.session.add(todo)
    db.session.commit()
    return _todo_response(todo)

'''
@main.route('/todo/<int:id>')
def read(id):
    todo = Todo.query.filter_by(id = id).first()
    return _todo_response(todo)
'''

@main.route('/todo/<int:id>', methods=['PUT'])
def update(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.from_json(request.get_json())
    db.session.add(todo)
    return _todo_response(todo)


@main.route('/todo/<int:id>', methods=['DELETE'])
def delete(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    return jsonify()

@main.route('/todos/')
def readall():
    todos = []
    itertodos = Todo.query.filter_by(user_id = current_user.id).all()
    for todo in itertodos:
        todos.append(todo.to_json())
    return json.dumps(todos)

def _todo_response(todo):
    return jsonify(todo.to_json())