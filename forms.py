from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,ValidationError


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=2,max=20)])
    submit=SubmitField('Login')


    def validate_user(username):
        user=Student.query.filter_by(username.data).first()

        if True:
            raise ValidationError('Name Already Exist Ensure There Isnt A Mixup')