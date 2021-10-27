from typing import Optional
from . import db



class Book(db.Model):
    title = db.Column(db.String(300), primary_key = True)
    authors = db.relationship("Author", backref='owner')
    available = db.Column(db.String(10))
    user = db.relationship("User", backref='user')
class Author(db.Model):
    name = db.Column(db.String(300),primary_key = True)
    book = db.Column(db.String, db.ForeignKey('book.title'))

    def __str__(self):
        return f'{self.name}'

class User(db.Model):
    name = db.Column(db.String(300),primary_key = True)
    book = db.Column(db.String, db.ForeignKey('book.title'))

    def __str__(self):
        return f'{self.name}'