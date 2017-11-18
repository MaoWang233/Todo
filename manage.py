#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Todo
from flask.ext.script import Manager, Shell

app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Todo=Todo)
manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
