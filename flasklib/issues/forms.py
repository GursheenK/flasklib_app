from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField
from wtforms.validators import ValidationError

class IssueForm(FlaskForm):
    days=StringField('Days')
    memberRadio=StringField()
    submit=SubmitField('Issue')

    def validate_memberRadio(self,memberRadio):
        if not memberRadio.data:
            flash('Select a member to proceed!','info')
            raise ValidationError()
    
class IssueReturnForm(FlaskForm):
    date=DateField('Date')
    memberRadio=StringField()
    
    def validate_memberRadio(self,memberRadio):
        if not memberRadio.data:
            flash('Select a member to proceed!','info')
            raise ValidationError()

    def validate_date(self,date):
        if not date.data:
            flash('Select a date to proceed!','info')
            raise ValidationError()