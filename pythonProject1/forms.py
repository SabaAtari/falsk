from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo
from model import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password =PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
class RegistrationForm(FlaskForm):
    email =StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('UserName',validators=[DataRequired()])
    password =PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Password must match!')])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField('Register')

    def check_email(self,field):
        if User.query.filter_by(email=field.data):
            raise ValidationError('Your email hae been already registered!')

class AddPost(FlaskForm):
    title= StringField('Title',validators=[DataRequired()])
    content= StringField('Content',validators=[DataRequired()])
    tags=StringField('Tags',validators=[DataRequired()])
    submit = SubmitField('Publish')

class AddComment(FlaskForm):
    content=StringField('Comment',validators=[DataRequired()])
    submit=SubmitField('Add')


