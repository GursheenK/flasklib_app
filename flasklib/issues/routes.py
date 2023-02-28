from flask import render_template,flash,url_for,redirect,request
from flasklib import db
from flasklib.models import Member,Book,BookIssue
from flasklib.issues.forms import IssueReturnForm,IssueForm
from datetime import datetime, timedelta
from flask_login import login_required

from flask import Blueprint

issues=Blueprint('issues',__name__)


@issues.route("/issue_book/<int:bid>",methods=['GET','POST'])
@login_required
def issue_book(bid):
    book=Book.query.get(bid)
    form=IssueForm()
    page=request.args.get('page',1,type=int)
    members=Member.query.paginate(per_page=10,page=page)
    print(members)
    if Member.query.first()==None:
        flash('No members added! Add one to issue the book.','danger')
        return redirect(url_for('books.viewbooks'))
    if form.validate_on_submit():
        mid=request.form['memberRadio']
        if book.availability<1:
            flash('Book not available!','danger')
        elif mid in book.borrowers.split(','):
            flash('Book already issued to this member!','info')
        else:
            if form.days.data:
                due_date=datetime.utcnow().date()+timedelta(days=int(form.days.data))
                issue=BookIssue(days=form.days.data,bid=bid,mid=mid,due_date=due_date)
            else:
                due_date=datetime.utcnow().date()+timedelta(days=7)
                issue=BookIssue(bid=bid,mid=mid,due_date=due_date)
            db.session.add(issue)
            book.availability-=1
            book.borrowers+=mid+','
            db.session.commit()
            flash('Book Issued!','success')
        return redirect(url_for('books.viewbooks'))
    return render_template('templates_issues/issue.html',title='Issue a Book',members=members,form=form,book=book)

@issues.route("/issue_return/<int:bid>",methods=['GET','POST'])
@login_required
def issue_return(bid):
    form=IssueReturnForm()
    issues=BookIssue.query.filter_by(bid=bid,returned=0).all()
    book=Book.query.get(bid)
    if form.validate_on_submit():
        mid=request.form['memberRadio']
        member=Member.query.get(mid)
        issue=BookIssue.query.filter_by(bid=bid,mid=mid,returned=0).first()
        issue.returned=1
        book.borrowers=book.borrowers.replace(mid+',','')
        book.availability+=1
        dtdiff=issue.due_date.date()-form.date.data
        fee=0
        if dtdiff.days<0:
            onedayfee=25
            fee=onedayfee*abs(dtdiff.days)
        issue.fee=fee
        if member.debt+issue.fee<=500:
            member.debt+=issue.fee
            member.dues=member.dues+str(issue.issue_id)+',' if issue.fee>0 else member.dues
        else:
            flash('Book return processed.Member debt exceeding 500.Cannot keep payment due.','danger')
            db.session.commit()
            return redirect(url_for('issues.issue_return',bid=bid))
        db.session.commit()
        flash('Book return processed. Please check member dues.','success')
        if request.form['submit_return'] == 'Pay Now':
            return redirect(url_for('members.member_info',mid=mid))
        return redirect(url_for('books.viewbooks'))
    return render_template('templates_issues/return.html',title='Issue a Book Return',form=form,issues=issues,book=book)