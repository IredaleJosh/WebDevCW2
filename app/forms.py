from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length, Optional

class LogInUser(FlaskForm):
    email = StringField("Email", validators=[Optional(),Length(min=10,max=25)])
    # Unsure of email length, validate by having previous stored @____.com
        # Change so it is optional for login, and neccessary for signup
    username = StringField("Username", validators=[InputRequired(),Length(min=5,max=15)])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=12,max=16)])
    # Hide password, Show password, Replace with * when typing

class TypeMessage(FlaskForm):
    text = TextAreaField(validators=[Optional(), Length(min=1,max=100)], render_kw={"placeholder": "Type Message Here"})

class ReviewGame(FlaskForm):
    rating = SelectField("Rating from 1 to 10: ", choices=[(str(i), str(i)) for i in range(1, 11)], validators=[InputRequired()])
    text = TextAreaField("Enter Review Here: ", validators=[InputRequired(), Length(min=1,max=100)], render_kw={"class": "review-label"})
