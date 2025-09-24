from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('commuter', 'Commuter'), ('owner', 'Owner')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ParkingSpotForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired(), Length(max=255)])
    timings = StringField('Timings (e.g., 08:00-22:00)', validators=[DataRequired()])
    price_per_hour = FloatField('Price per hour', validators=[DataRequired()])
    availability = BooleanField('Available', default=True)
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Add / Update Spot')

class BookingForm(FlaskForm):
    start_time = DateTimeField('Start Time (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_time = DateTimeField('End Time (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Book Now')