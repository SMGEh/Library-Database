from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, DateField, SelectField, TextAreaField, IntegerField

from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_bar=StringField('Search Item Name or Creator', render_kw={"placeholder": "Enter book name or author","size":"60px","height":"60px"})
    search_button=SubmitField('Search',render_kw={"size":"60px", "height":"60px"})


class LoginForm(FlaskForm):
    number = StringField('Library Number:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class Register(FlaskForm):
    unregister_button = SubmitField("unregister")
    submit_button = SubmitField("Register")

class LogoutForm(FlaskForm):
    logout_button = SubmitField("Logout")

class CheckoutForm(FlaskForm):
    renew = SubmitField("Renew")
    renewReason=TextAreaField()
    submit_button = SubmitField("Checkout")
    returnItem = SubmitField("return")

class Volunteer(FlaskForm):
    availability=TextAreaField()

    experience=TextAreaField()

    interests=TextAreaField()

    startDate=DateField()

    endDate=DateField()

    submit_button = SubmitField("Volunteer")

    unregister_button = SubmitField("unregister")


class DonateForm(FlaskForm):
    dropdown=SelectField('Item Type',choices=[('Book','book'),('Magazine','magazine'),('CD','CD'),('Record','record'),('Journal','journal'),('Movie','movie')])
    title=StringField('Title', validators=[DataRequired()])
    description=TextAreaField('Description', validators=[DataRequired()])
    donateDate=DateField(validators=[DataRequired()])

    submit_button = SubmitField('Donate')