from flask import render_template,flash,url_for,redirect,request,make_response
from flasklib import db
from flasklib.models import Member,Book,BookIssue
from flasklib.members.forms import MemberForm
from flasklib.issues.forms import IssueForm
from datetime import datetime
import pdfkit
from flask_login import login_required

from flask import Blueprint

members=Blueprint('members',__name__)

@members.route("/members")
@login_required
def viewmembers():
    page=request.args.get('page',1,type=int) 
    keyword=request.args.get('keyword','',type=str)
    members=Member.query.paginate(per_page=10,page=page)
    allmemberslist=Member.query.all()
    allmembernames=[m.mname for m in allmemberslist]
    if keyword!='':
        return redirect(url_for('members.search_member',page=page,members=members,keyword=keyword))
    return render_template('templates_members/members.html',title='Members',members=members,allmembernames=allmembernames)

@members.route("/member_info/<int:mid>",methods=['GET','POST'])
@login_required
def member_info(mid):
    member=Member.query.get(mid)
    borrowed=[]
    for i in member.issues:
        if i.returned==0:
            borrowed.append(Book.query.get(i.bid))
    dues=member.dues.split(',')
    dues.pop()
    issuedues=[]
    for due in dues:
        issuedues.append(BookIssue.query.get(due))
    if request.method=='POST':
        issue_id=request.args.get('issue_id')
        if issue_id=='0':
            member.dues=''
            member.debt=0
            rendered=render_template('templates_issues/invoicepdf.html',member=member,issues=issuedues,date=datetime.utcnow().date())
        else:
            issue=BookIssue.query.get(issue_id)
            member.dues=member.dues.replace(issue_id+',','')
            member.debt=member.debt-issue.fee
            rendered=render_template('templates_issues/invoicepdf.html',member=member,issues=issuedues,date=datetime.utcnow().date())
        db.session.commit()
        flash('Payment successful!','success')
        config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        pdf=pdfkit.from_string(rendered,False,configuration=config)
        response=make_response(pdf)
        response.headers['Content-Type']='application/pdf'
        response.headers['Content-Disposition']='inline; filename=generated.pdf'
        return response
    return render_template('templates_members/member_info.html',title='Member Info',member=member,borrowed=borrowed,issuedues=issuedues)

@members.route("/add_member",methods=['GET','POST'])
@login_required
def add_member():
    form=MemberForm()
    if form.validate_on_submit():
        member=Member(mname=form.mname.data,email=form.email.data,contact=form.contact.data)
        db.session.add(member)
        db.session.commit()
        flash('Member Added!','success')
        return redirect(url_for('members.viewmembers'))
    return render_template('templates_members/add_member.html',title='Add Member',form=form)

@members.route("/update_member/<int:mid>",methods=['GET','POST'])
@login_required
def update_member(mid):
    form=MemberForm()
    member=Member.query.get(mid)
    if request.method == 'GET':
        form.mname.data=member.mname
        form.email.data=member.email
        form.contact.data=member.contact
    if form.validate_on_submit():
        member.mname=form.mname.data
        member.email=form.email.data
        member.contact=form.contact.data
        db.session.commit()
        flash('Member Updated!','success')
        return redirect(url_for('members.viewmembers'))
    
    return render_template('templates_members/add_member.html',title='Update Member',form=form)


@members.route("/delete_member/<int:mid>",methods=['POST'])
@login_required
def delete_member(mid):
    member=Member.query.get(mid)
    db.session.delete(member)
    db.session.commit()
    flash('Member Removed!','success')
    return redirect(url_for('members.viewmembers'))

@members.route("/search_member/<string:keyword>",methods=['GET','POST'])
@members.route("/issue_book/<int:bid>/search_member/<string:keyword>",methods=['GET','POST'])
@login_required
def search_member(keyword,bid=0):
    rule=request.url_rule
    keyword=request.form['searchbar'] if keyword=='None' else keyword
    page=request.args.get('page',1,type=int)
    members=Member.query.filter(Member.mname.contains(keyword.strip())).paginate(per_page=10,page=page)
    if 'issue_book' in rule.rule:
        form=IssueForm()
        return render_template('templates_issues/issue.html',title='Issue Book',form=form,members=members,keyword=keyword,bid=bid)
    return render_template('templates_members/members.html',title='Members',members=members,keyword=keyword)
