from flask_login import UserMixin
from flasklib import db,login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False) # since bcrypt returns a hash of the password 60 chars long

    def __repr__(self):
        return f"Admin('{self.id}','{self.username}')"
    
class Member(db.Model):
    mid=db.Column(db.Integer,primary_key=True)
    mname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    contact=db.Column(db.String(12),nullable=False)
    date_added=db.Column(db.DateTime,default=datetime.utcnow)
    debt=db.Column(db.Float,nullable=False,default=0)
    dues=db.Column(db.String,default='')

    books=db.relationship('Book',backref='issued_to',lazy=True)
    issues=db.relationship('BookIssue',backref='issues',lazy=True)

    def __repr__(self) -> str:
        return f'Member({self.mid,self.mname})'

class Book(db.Model):
    bid=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String,nullable=False)
    authors=db.Column(db.String,nullable=False)
    average_rating=db.Column(db.String,nullable=False)
    isbn=db.Column(db.String,nullable=False)
    publisher=db.Column(db.String,nullable=False)
    publish_date=db.Column(db.String,nullable=False)
    quantity=db.Column(db.Integer,nullable=False,default=5)
    availability=db.Column(db.Integer,nullable=False,default=5)

    borrowers=db.Column(db.String,db.ForeignKey('member.mid'),default='')

    def __repr__(self) -> str:
        return f'Book({self.bid,self.title})'

class BookIssue(db.Model):
    issue_id=db.Column(db.Integer,primary_key=True)
    days=db.Column(db.Integer,nullable=False,default=7)
    bid=db.Column(db.Integer,nullable=False)
    mid=db.Column(db.Integer,db.ForeignKey('member.mid'),default='')
    issue_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    due_date=db.Column(db.DateTime,nullable=False)
    fee=db.Column(db.Float)
    returned=db.Column(db.Boolean,nullable=False,default=0)

    def __repr__(self) -> str:
        return f'BookIssue({self.issue_id,self.bid,self.issue_date})'
