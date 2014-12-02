from flask import render_template, session, redirect, url_for, flash
from . import main
from .forms import *
from .. import db
from ..models import * 
from flask.ext.login import login_required, current_user

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    form = Search()
    if form.validate_on_submit():
        book = Book.query.filter(Book.title.contains(form.pattern.data)).all()
        author = Author.query.filter(Author.name.contains(form.pattern.data)).all()
        query = form.pattern.data
        if book:
            return render_template('index.html', result=book, form=form, formName='book', query=query)
        elif author:
            return render_template('index.html', result=author, form=form, formName='author', query=query)
        else:
            flash('No records found')
            return render_template('index.html', form=form, query=query)
    return render_template('index.html', form=form)

@main.route('/add/<item>', methods=['GET', 'POST'])
@login_required
def add(item):
    if (item == 'book'):
        form = AddBook()
    elif (item == 'author'):
        form = AddAuthor()
    if form.validate_on_submit():
        if (item == 'book'):
            bookExist = Book.query.filter(Book.title==form.title.data).first()
            if bookExist is not None:
                flash('Book already in library')
                return render_template('add.html', form=form, formName=item)              
            else:
                book = Book(form.title.data, [])
                formAuthors = form.author.data.split(', ')
                for author in formAuthors:
                    authorExist = Author.query.filter(Author.name==author).first()
                    if authorExist is not None:
                        book.authors.append(authorExist)
                    else:
                        newAuthor = Author(author)
                        db.session.add(newAuthor)
                        book.authors.append(newAuthor)
                db.session.add(book)
                flash('Book has been added.')
        elif (item == 'author'):
            authorExist = Author.query.filter(Author.name==form.name.data).first()
            if authorExist is not None:
                flash('Author is already in library!')
                return render_template('add.html', form=form, formName=item)
            else:
                author = Author(form.name.data)
                db.session.add(author)
                flash('Author has been added.')
        return redirect(url_for('.index'))
    return render_template('add.html', form=form, formName=item)

@main.route('/<action>/<item>', methods=['GET', 'POST'])
@login_required
def search_item(action, item):
    form = Search()
    if form.validate_on_submit():
        book = Book.query.filter(Book.title.contains(form.pattern.data)).all()
        author = Author.query.filter(Author.name.contains(form.pattern.data)).all()
        query = form.pattern.data
        if (action == 'edit'):
            if (item == 'book'):
                if book:
                    return render_template('edit.html', result=book, form=form, formName=item, query=query, action=action)
                else:
                    flash('No records found')
                    return render_template('edit.html', form=form, formName=item, action=action)
            elif (item == 'author'):
                if author:
                    return render_template('edit.html', result=author, form=form, formName=item, query=query, action=action)
                else:
                    flash('No records found')
                    return render_template('edit.html', form=form, formName=item, action=action)
        elif action == 'remove':
            if (item == 'book'):
                if book:
                    return render_template('edit.html', result=book, form=form, formName=item, query=query, action=action)
                else:
                    flash('No records found')
                    return render_template('edit.html', form=form, formName=item, action=action)
            elif (item == 'author'):
                if author:
                    return render_template('edit.html', result=author, form=form, formName=item, query=query, action=action)
                else:
                    flash('No records found')
                    return render_template('edit.html', form=form, formName=item, action=action)
    return render_template('edit.html', form=form, formName=item, action=action)

@main.route('/edit/<item>/<int:itemid>', methods=['GET', 'POST'])
@login_required
def edit_item(item, itemid):
    if (item == 'book'):
        book = Book.query.filter(Book.id==int(itemid)).first()
        form = EditBook()
        if form.validate_on_submit():
            bookTitleExist = Book.query.filter(Book.title==form.title.data).first()
            if (bookTitleExist) is not None and (bookTitleExist.title != form.title.data):
                flash('Book is already in library!')
                return render_template('edit_item.html', form=form, formName=item)
            else:
                bookAuthors = ', '.join(map(str, book.authors)).split(', ')
                formAuthors = form.author.data.split(', ')
                for author in book.authors:
                    book.authors.remove(author)
                for author in formAuthors:
                    authorExist = Author.query.filter(Author.name==author).first()
                    if authorExist is None:
                        createAuthor = Author(author)
                        db.session.add(createAuthor)
                        book.authors.append(createAuthor)
                    else:
                        book.authors.append(authorExist)
                book.title=form.title.data
                db.session.add(book)
                flash('Book info has been updated!')
                return redirect(url_for('.index'))
        form.title.data=book.title
        try:
            form.author.data = ', '.join(map(str, book.authors))
        except:
            form.author.data = ''
    elif (item == 'author'):
        author = Author.query.filter(Author.id==int(itemid)).first()
        form = EditAuthor()
        if form.validate_on_submit():
            authorExist = Author.query.filter(Author.name==str(form.name.data)).first()
            if (authorExist is not None) and (authorExist.name != form.name.data):
                flash('Author is already in library!')
                return render_template('edit_item.html', form=form, formName=item)
            else:
                db.session.query(Author).filter(Author.id==int(itemid)).update({Author.name: str(form.name.data)})
                flash('Author info has been updated!')
            return redirect(url_for('.index'))
        form.name.data = author.name
    return render_template('edit_item.html', form=form, formName=item)

@main.route('/remove/<item>/<int:itemid>', methods=['GET', 'POST'])
@login_required
def remove(item, itemid):
    if (item == 'book'):
        book = Book.query.filter(Book.id==int(itemid)).first()
        form = RemoveBook()
        if form.validate_on_submit():
            db.session.delete(book)
            flash('Book has been removed!')
            return redirect(url_for('.index'))
        form.title.data = book.title
        try:
            form.author.data = ', '.join(map(str, book.authors))
        except:
            form.author.data = ''
    elif (item == 'author'):
        author = Author.query.filter(Author.id==int(itemid)).first()
        form = RemoveAuthor()
        if form.validate_on_submit():
            db.session.delete(author)
            flash('Author has been removed!')
            return redirect(url_for('.index'))
        form.name.data = author.name
    return render_template('remove_item.html', form=form, formName=item)
