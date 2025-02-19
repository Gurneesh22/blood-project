from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from application.models import User

class RegisterForm(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    dob = DateField(label='Date of Birth:', format='%Y-%m-%d', validators=[DataRequired()])
    blood_group = SelectField(label='Blood Group:', 
                            choices=[
                                ('A+', 'A+'), ('A-', 'A-'),
                                ('B+', 'B+'), ('B-', 'B-'),
                                ('O+', 'O+'), ('O-', 'O-'),
                                ('AB+', 'AB+'), ('AB-', 'AB-')
                            ],
                            validators=[DataRequired()])
    city = StringField(label='City:', validators=[DataRequired()])
    gender = SelectField(label='Gender:',
                        choices=[
                            ('male', 'Male'),
                            ('female', 'Female'),
                            ('other', 'Other')
                        ],
                        validators=[DataRequired()])
    contact_number = StringField(label='Contact Number:', validators=[
        DataRequired(),
        Regexp(r'^\d{10}$', message="Contact number must be 10 digits.")
    ])
    submit = SubmitField(label='Create Account')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')


class LoginForm(FlaskForm):
    email_address = StringField(label='Email:', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')