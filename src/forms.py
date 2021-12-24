from re import sub
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, EqualTo, Length

class RegisterForm(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired()])
    first_name = StringField("Enter your first name", validators=[DataRequired()])
    middle_name = StringField("Enter your middle name")
    last_name = StringField("Enter your last name", validators=[DataRequired()])
    sex = StringField("Enter your sex", validators=[DataRequired()])
    birthdate = DateField("Enter your birthdate", validators=[DataRequired()])
    password = PasswordField("Enter your password", validators=[DataRequired()])
    password_check = PasswordField("Re-enter password", validators=[DataRequired()])
    submit = SubmitField("Register")
