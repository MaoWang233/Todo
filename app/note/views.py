from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import note
from .. import db
from ..models import User


@note.route('/')
@login_required
def todo():

    return render_template('todo.html')