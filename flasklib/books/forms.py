from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,FloatField,SubmitField
from wtforms.validators import DataRequired,ValidationError

class BookForm(FlaskForm):
    title=StringField('Title')
    author=StringField('Author')
    amount=IntegerField('Amount')
    isbn=StringField('Isbn')

class BookUpdateForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    authors=StringField('Authors',validators=[DataRequired()])
    publisher=StringField('Publisher',validators=[DataRequired()])
    publish_date=StringField('Publish Date',validators=[DataRequired()])
    average_rating=FloatField('Rating')
    quantity=IntegerField('Quantity')
    submit=SubmitField('Update')

    def validate_quantity(self,quantity):
        if quantity.data and quantity.data<0:
            raise ValidationError('Must be 0 or positive.')