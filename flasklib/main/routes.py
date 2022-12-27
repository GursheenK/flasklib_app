import html
from flask import render_template,flash,url_for,redirect,request,make_response
from flasklib import db,bcrypt
from flasklib.models import Member,Book,BookIssue,Admin
from flasklib.main.forms import AdminLoginForm
from datetime import datetime, timedelta
from sqlalchemy import func,desc
import pdfkit
from flask_login import login_required,login_user,logout_user

from flask import Blueprint


main=Blueprint('main',__name__)

@main.route("/",methods=['GET','POST'])
def login():
    adminform=AdminLoginForm()
    if request.method=='POST' and request.form['submit'] == 'Admin Login':
        if adminform.validate_on_submit():
            admin= Admin.query.filter_by(username=adminform.username.data).first()
            if admin and bcrypt.check_password_hash(admin.password,adminform.password.data):
                login_user(admin)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Incorrect Admin Credentials','danger')
    if request.method=='POST' and request.form['submit'] == 'Browse Books':
                return redirect(url_for('main.guest'))
    return render_template('templates_main/login.html',adminform=adminform)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route("/guest",methods=['GET','POST'])
def guest():
    page=request.args.get('page',1,type=int)
    books=Book.query.filter(Book.availability>0).paginate(per_page=9,page=page)
    allbookslist=Book.query.all()
    allbooknames=[b.title for b in allbookslist]
    keyword=request.args.get('keyword','',type=str)
    if request.method=='POST':
        keyword=request.form['searchbar']
    if keyword!='':
        books=Book.query.filter(Book.availability>0,Book.title.contains(keyword.strip())|Book.authors.contains(keyword.strip())).paginate(per_page=9,page=page)
    return render_template('templates_main/guest.html',title='Books',books=books,keyword=keyword,allbooknames=allbooknames)


@main.route("/home")
@login_required
def home():
    totalb=db.session.query(Book).count()
    totali=len(BookIssue.query.filter_by(returned=0).all())
    totalm=db.session.query(Member).count()
    restock=Book.query.filter_by(quantity=0).limit(5)#quantity=0 for restock
    startdate=datetime.now().date()-timedelta(days=6)
    dbweek=db.session.query(BookIssue.issue_date,func.count(BookIssue.issue_id).label('qty')).filter(func.date(BookIssue.issue_date)>=startdate).group_by(func.date(BookIssue.issue_date)).all()
    weeklyissues=[(startdate+timedelta(days=i),0) for i in range(7)]
    for j in dbweek:
        if (j[0].date(),0) in weeklyissues:
            index=weeklyissues.index((j[0].date(),0))
            weeklyissues[index]=(j[0].date(),j[1])
    newmembers=Member.query.order_by(desc('date_added')).limit(5)
    recentissues=BookIssue.query.order_by(desc('issue_date')).limit(5)
    return render_template('templates_main/home.html',title='Home',totalb=totalb,totali=totali,totalm=totalm,restock=restock,weeklyissues=weeklyissues,newmembers=newmembers,recentissues=recentissues)

@main.route('/reports',methods=['GET','POST'])
@login_required
def reports():
    popular=db.session.query(BookIssue.bid,func.count(BookIssue.issue_id).label('qty')).group_by(BookIssue.bid).order_by(desc('qty')).limit(10) 
    books=[]
    bcount=[]
    for p in popular:
        books.append(Book.query.get(p[0]))
        bcount.append(p[1])
    if len(bcount)==0:
        bcount=[1,1,1,1,1]
    most_paying=db.session.query(BookIssue.mid,func.sum(BookIssue.fee)).filter_by(returned=1).group_by(BookIssue.mid).all()
    members=[[Member.query.get(m[0]),m[1]] for m in most_paying]
    for i in range(len(members)):
        members[i][1]=members[i][1]-members[i][0].debt
    activity={}
    for m in members:
        issues=BookIssue.query.filter_by(mid=m[0].mid).all()
        monthwise=[0]*12
        for i in issues:
            monthwise[(i.issue_date.month)-1]+=1
        activity[m[0].mid]=monthwise
    if request.method=='POST':
        if request.args['flag']=='bksreport':
            rendered=render_template('templates_reports/bksreportpdf.html',books=books,bcount=bcount)
        if request.args['flag']=='memsreport':
            rendered=render_template('templates_reports/memsreportpdf.html',members=members[:10])
        config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf/bin")
        pdf=pdfkit.from_string(rendered,False,configuration=config)
        response=make_response(pdf)
        response.headers['Content-Type']='application/pdf'
        response.headers['Content-Disposition']='inline; filename=generated.pdf'
        return response
    return render_template('templates_reports/reports.html',title='Reports',books=books[:5],bcount=bcount[:5],members=members,activity=activity)

@main.route("/about")
@login_required
def about():
    return render_template('templates_main/about.html',title='About')