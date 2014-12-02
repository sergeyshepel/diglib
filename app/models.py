import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager

publishing = db.Table('publishing', 
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

class Author(db.Model):
    __tablename__ = 'author'            
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    @staticmethod
    def add_authors(count=100):
        from sqlalchemy.exc import IntegrityError
        import forgery_py

        for i in range(count):
            a = Author(name=forgery_py.name.full_name())
            db.session.add(a)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Book(db.Model):
    __tablename__ = 'book'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    authors = db.relationship('Author', secondary=publishing, backref=db.backref('books', lazy='joined'), lazy='dynamic')
    
    @staticmethod
    def add_books():
        from sqlalchemy.exc import IntegrityError
        from random import randint
        import forgery_py
        
        for author in Author.query.all():
            b = Book(title=forgery_py.lorem_ipsum.title(randint(1, 5)), authors=[author])
            db.session.add(b)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, title, authors):
        self.title = title
        self.authors = authors

    def __repr__(self):
        return self.title

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))

    @staticmethod
    def add_admin():
        from sqlalchemy.exc import IntegrityError
        u = User(username='admin', password='admin', name='Sergey Shepel')
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

login_manager.anonymous_user = AnonymousUser
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
