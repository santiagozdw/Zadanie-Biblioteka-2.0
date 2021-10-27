from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Book, Author, User
from .schemas import BookSchema
import requests
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])

def home():
    books = Book.query.all()
    books_lst = []
    for book in books:
        books_lst.append(BookSchema(book))
    return render_template("home.html", books = books_lst, books_no = len(books))



@views.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method =='POST':
        title = request.form.get('title')
        authors = request.form.get('authors')
        available = request.form.get('available')
        for item in request.form.items():
            if not item[1]:
                flash(f'Missing requied field "{item[0].capitalize()}"', category='error')
        if all(request.form.values()):
            new_book = Book(title=title,
                            available=available)
            author = Author(name = authors, book = title)
            db.session.add(author)
            db.session.add(new_book)
            
            db.session.commit()
            flash(f'book added (Title:{new_book.title})')
            books = Book.query.all()
            books_lst = []
            for book in books:
                books_lst.append(BookSchema(book))            
            return render_template("home.html", books=books_lst, books_no=len(books))
    return render_template('add.html')

@views.route('/edit', methods = ['GET', 'POST'])
def edit():
    if request.method == 'POST':  
        print(request.args)
        n_title = request.form.get('title')
        n_available = request.form.get('available')
        print(n_title, n_available)
        book = Book.query.get(n_title)
        if book:
            book = Book.query.get(n_title)
            book.available = n_available
            db.session.commit()
            flash(f'book updated ({n_title})')
        return home()
    else:
        book = None
        print(request.args)
        if request.args:
            book = BookSchema(Book.query.get(request.args["title"]))
        return render_template('edit.html', book = book)

@views.route('/lend', methods = ['GET', 'POST'])
def lend():
    if request.method == 'POST':  
        print(request.args)
        n_title = request.form.get('title')
        n_available = request.form.get('available')
        n_user = request.form.get('user')
        book = Book.query.get(n_title)
        if book:
            book = Book.query.get(n_title)
            user = User(name = n_user, book = n_title)
            if n_user not in [user.name for user in User.query.all()]:
                book.available = n_available
                db.session.add(user)
                db.session.commit()
                flash(f'book lended ({n_title} -> {n_user})')
            else:
                flash(f'user already lended other book')
            
        return home()
    else:
        book = None
        print(request.args)
        if request.args:
            book = BookSchema(Book.query.get(request.args["title"]))
        return render_template('lend.html', book = book)

@views.route('/return', methods = ['GET', 'POST'])
def return_book():
    print(request.args)
    n_title = request.args['title']
    n_user = request.args['user']
    print(n_title, n_user)
    book = Book.query.get(n_title)
    if book:
        book = Book.query.get(n_title)
        book.available = 'on'
        user = User.query.get(n_user)
        db.session.delete(user)
        db.session.commit()
        flash('book returned')
    else:
        flash(f'some error')
            

    return redirect(url_for("views.home"))