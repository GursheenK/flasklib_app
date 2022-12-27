from flask import render_template,flash,url_for,redirect,request
from flasklib import db
from flasklib.models import Book
from flasklib.books.forms import BookForm,BookUpdateForm
import requests,json
from flask_login import login_required

from flask import Blueprint

books=Blueprint('books',__name__)

@books.route("/books",methods=['GET','POST'])
@login_required
def viewbooks():
    page=request.args.get('page',1,type=int)
    keyword=request.args.get('keyword','',type=str)
    books=Book.query.paginate(per_page=10,page=page)
    allbookslist=Book.query.all()
    allbooknames=[b.title for b in allbookslist]
    if keyword!='':
        return redirect(url_for('books.search_book',page=page,keyword=keyword,books=books))
    return render_template('templates_books/books.html',title='Books',books=books,allbooknames=allbooknames)

def getbooks(title,author,amount,isbn):
    books=[]
    full_pages=amount//20
    for i in range(1,full_pages+1):
        path='https://frappe.io/api/method/frappe-library?page='+str(i)
        if title:
            path+='&title='+title
        if author:
            path+='&authors='+author
        if isbn:
            path+='&isbn='+isbn
        req=requests.get(path)
        books+=json.loads(req.content)['message']
    path='https://frappe.io/api/method/frappe-library?page='+str(full_pages+1)
    if title:
        path+='&title='+title
    if author:
        path+='&authors='+author
    if isbn:
        path+='&isbn='+isbn
    req=requests.get(path)
    temp=json.loads(req.content)['message']
    books+=temp[0:amount%20]
    return books

@books.route("/add_book",methods=['GET','POST'])
@login_required
def add_book():
    form=BookForm()
    if request.method=='POST':
        title=request.form['title']
        author=request.form['author']
        amt=request.form['amount'] if request.form['amount'] else 20
        amt=int(amt)
        isbn=request.form['isbn']
        books=getbooks(title,author,amt,isbn)
        if request.form['submit_button'] == 'Search':
            return render_template('templates_books/add_book.html',title="Add Books",form=form,books=books)
        if request.form['submit_button'] == 'Import All':
            if len(books)<=0:
                flash('No books to import.','info')
            else:
                for b in books:
                    book=Book(bid=b['bookID'],title=b['title'],authors=b['authors'],average_rating=b['average_rating'],isbn=b['isbn'],publisher=b['publisher'],publish_date=b['publication_date'])
                    bookindb=Book.query.get(b['bookID'])
                    if not bookindb:
                        db.session.add(book)
                        db.session.commit()
                flash('Books added successfully.','success')
    return render_template('templates_books/add_book.html',form=form,title="Add Books")

@books.route("/add_onebook/<string:isbn>",methods=['GET','POST'])
@login_required
def add_onebook(isbn):
    req=requests.get('https://frappe.io/api/method/frappe-library?isbn='+isbn)
    b=json.loads(req.content)['message'][0]
    book=Book(title=b['title'],authors=b['authors'],average_rating=b['average_rating'],isbn=b['isbn'],publisher=b['publisher'],publish_date=b['publication_date'])
    bookindb=Book.query.get(b['bookID'])
    if not bookindb:
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully.','success')
    else:
        flash('Book is already added!','info')
    return redirect(url_for('books.add_book'))

@books.route("/update_book/<int:bid>",methods=['GET','POST'])
@login_required
def update_book(bid):
    form=BookUpdateForm()
    book=Book.query.get(bid)
    if request.method == 'GET':
        form.title.data=book.title
        form.authors.data=book.authors
        form.publisher.data=book.publisher
        form.publish_date.data=book.publish_date
        form.average_rating.data=book.average_rating
        form.quantity.data=book.quantity
    if form.validate_on_submit():
        book.title=form.title.data
        book.authors=form.authors.data
        book.publisher=form.publisher.data
        book.publish_date=form.publish_date.data
        book.average_rating=form.average_rating.data
        book.quantity=form.quantity.data
        db.session.commit()
        flash('Book Updated!','success')
        return redirect(url_for('books.viewbooks'))
    
    return render_template('templates_books/update_book.html',title='Update book',form=form)


@books.route("/delete_book/<int:bid>",methods=['POST'])
@login_required
def delete_book(bid):
    book=Book.query.get(bid)
    db.session.delete(book)
    db.session.commit()
    flash('Book Removed!','success')
    return redirect(url_for('books.viewbooks'))

@books.route("/search_book/<string:keyword>",methods=['GET','POST'])
@login_required
def search_book(keyword):
    keyword=request.form['searchbar'] if keyword=='None' else keyword
    page=request.args.get('page',1,type=int)
    books=Book.query.filter((Book.title.contains(keyword.strip()))|(Book.authors.contains(keyword.strip()) )).paginate(per_page=10,page=page)
    
    return render_template('templates_books/books.html',title='Books',books=books,keyword=keyword)
