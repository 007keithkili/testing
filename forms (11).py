from flask_wtf import FlaskForm
from wtforms import DateField, EmailField, FileField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, NumberRange, Optional

SUBJECT_CHOICES = [
    ('General Inquiry', 'General Inquiry'),
    ('Booking Request', 'Booking Request'),
    ('Partnership', 'Partnership'),
    ('Other', 'Other'),
]


class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = EmailField('Your Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    travellers = StringField('Number of travellers', validators=[Optional()])
    destination = StringField('Destination', validators=[Optional()])
    subject = SelectField('Subject', choices=SUBJECT_CHOICES, validators=[DataRequired()])
    message = TextAreaField('Your Message', validators=[DataRequired()])


class NewsletterForm(FlaskForm):
    email = EmailField('Your email address', validators=[DataRequired(), Email()])


class BookingForm(FlaskForm):
    item_type = StringField('Item type', validators=[Optional()])
    item_id = IntegerField('Item id', validators=[Optional()])
    item_title = StringField('Item', validators=[Optional()])
    name = StringField('Full name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    travellers = IntegerField('Travellers', default=1, validators=[Optional(), NumberRange(min=1, max=50)])
    travel_date = DateField('Preferred travel date', validators=[Optional()])
    message = TextAreaField('Message', validators=[Optional()])


class JobApplicationForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    message = TextAreaField('Cover note', validators=[Optional()])
    cv = FileField('CV / supporting document', validators=[Optional()])
