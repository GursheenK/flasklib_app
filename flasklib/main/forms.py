from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length

class AdminLoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20,message='Length of username must be 5-20 characters.')])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=5,message='Password must be atleast 5 characters long.')])
    submit=SubmitField('Admin Login')