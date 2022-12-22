from flasklib import create_app,db,bcrypt
from flasklib.models import Admin

app=create_app()

if __name__=='__main__':
    with app.app_context():
        db.create_all()
        if Admin.query.first()==None:
            passwordhash = bcrypt.generate_password_hash('password').decode('utf-8')
            admin=Admin(username='admin',password=passwordhash)
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
