from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from wtforms.validators import DataRequired, Email, NumberRange

class MemberForm(FlaskForm):
    mname=StringField('Name',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    contact=IntegerField('Contact No',validators=[DataRequired(),NumberRange(min=0, max=10000000000, message='Invalid length')])
    submit=SubmitField('Submit')