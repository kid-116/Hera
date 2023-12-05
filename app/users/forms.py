from wtforms import Form, StringField, PasswordField, validators, IntegerField

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    phone = IntegerField('Number',
                         [validators.NumberRange(min=10**9, max=10**10 - 1)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
