#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Author, User, Book
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Author=Author, Book=Book)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Author, Book, User
    upgrade()
    Author.add_authors()
    Book.add_books()
    User.add_admin()

if __name__ == '__main__':
    manager.run()
