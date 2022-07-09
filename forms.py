from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import InputRequired

class NewUserForm(FlaskForm):
    '''Form for new user'''

    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class SignInForm(FlaskForm):
    '''Form for sign in'''

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class NewPostForm(FlaskForm):
    '''Form for new post'''

    content = TextAreaField('Content')
    movie_id = HiddenField('movie_id')
    type = HiddenField('type')

class SearchForm(FlaskForm):
    '''Form for searching movies or tv shows'''

    content_type = SelectField('Movie or TV Show?', choices=[('movie', 'Movie'), ('show', 'TV Show')])
    search = StringField('Search...')

class SelectForm(FlaskForm):
    '''Form to select a movie or tv show'''

    movie_id = HiddenField('movie_id')
    movie_or_tv = HiddenField('movie_or_tv')

class EditPostForm(FlaskForm):
    '''Form to edit a post'''

    content = TextAreaField('Content')