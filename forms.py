from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional


def lines_to_list(value):
    """Turn a textarea value into a clean list of strings."""
    if not value:
        return []
    items = []
    for line in value.replace('\r\n', '\n').split('\n'):
        line = line.strip()
        if line:
            items.append(line)
    return items


class DestinationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    slug = StringField('Slug', validators=[Optional()])
    tag = StringField('Category', default='Safari', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    highlights = TextAreaField('Highlights (one per line)', validators=[Optional()])
    price = StringField('Price label (e.g. $1,299)', validators=[Optional()])
    price_value = IntegerField('Price (numeric)', default=0, validators=[Optional(), NumberRange(min=0)])
    duration_days = IntegerField('Duration in days', default=1, validators=[Optional(), NumberRange(min=1)])
    location = StringField('Location', validators=[Optional()])
    sort_order = IntegerField('Sort order', default=0, validators=[Optional()])
    is_featured = BooleanField('Show on home page')
    is_active = BooleanField('Published', default=True)


class PackageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    slug = StringField('Slug', validators=[Optional()])
    tagline = StringField('Tagline', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    image_url = StringField('Image URL', validators=[Optional()])
    price = StringField('Price label (e.g. $2,499)', validators=[Optional()])
    price_value = IntegerField('Price (numeric)', default=0, validators=[Optional(), NumberRange(min=0)])
    days = IntegerField('Days', default=1, validators=[Optional(), NumberRange(min=1)])
    nights = IntegerField('Nights', default=0, validators=[Optional(), NumberRange(min=0)])
    features = TextAreaField('Features (one per line)', validators=[Optional()])
    tags = TextAreaField('Tags (comma separated)', validators=[Optional()])
    comparison = TextAreaField('Comparison rows (one per line, "Label: Value")', validators=[Optional()])
    highlight = StringField('Highlight label (e.g. Most Popular)', validators=[Optional()])
    sort_order = IntegerField('Sort order', default=0, validators=[Optional()])
    is_featured = BooleanField('Show on home page')
    is_active = BooleanField('Published', default=True)


class ExperienceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    duration = StringField('Duration', validators=[Optional()])
    highlights = TextAreaField('Highlights', validators=[Optional()])
    price = StringField('Price label', validators=[Optional()])
    image_url = StringField('Image URL', validators=[Optional()])
    sort_order = IntegerField('Sort order', default=0, validators=[Optional()])
    is_active = BooleanField('Published', default=True)


class JobForm(FlaskForm):
    title = StringField('Job title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[Optional()])
    summary = TextAreaField('Job summary', validators=[Optional()])
    responsibilities = TextAreaField('Responsibilities (one per line)', validators=[Optional()])
    qualifications = TextAreaField('Qualifications (one per line)', validators=[Optional()])
    location = StringField('Location', default='Narok, Kenya', validators=[Optional()])
    is_active = BooleanField('Accepting applications', default=True)


class LegalPageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    hero_title = StringField('Hero title', validators=[Optional()])
    hero_subtitle = StringField('Hero subtitle', validators=[Optional()])
    content = TextAreaField('Content (HTML allowed)', validators=[Optional()])


class SiteSettingsForm(FlaskForm):
    company_name = StringField('Company name', validators=[Optional()])
    tagline = StringField('Tagline', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    hours = StringField('Opening hours', validators=[Optional()])
    whatsapp = StringField('WhatsApp number', validators=[Optional()])
    facebook = StringField('Facebook URL', validators=[Optional()])
    twitter = StringField('Twitter/X URL', validators=[Optional()])
    instagram = StringField('Instagram URL', validators=[Optional()])
    youtube = StringField('YouTube URL', validators=[Optional()])
    pinterest = StringField('Pinterest URL', validators=[Optional()])
    admin_email = StringField('Administrator email (receives notifications)', validators=[Optional()])
    hero_title = StringField('Home hero title', validators=[Optional()])
    hero_subtitle = StringField('Home hero subtitle', validators=[Optional()])
    logo_url = StringField('Logo URL', validators=[Optional()])
