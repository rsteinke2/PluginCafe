from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me In!")

# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

class CreateCafeForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    map_url = StringField("Cafe map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    has_toilet = StringField("Does it have toilet?", validators=[DataRequired()])
    has_wifi = StringField("Does it have Wifi?", validators=[DataRequired()])
    has_sockets = StringField("Does it have sockets?", validators=[DataRequired()])
    can_take_calls = StringField("Can people take calls?", validators=[DataRequired()])
    coffee_price = StringField("Coffee price:", validators=[DataRequired()])
    rating = StringField("Rating:", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
