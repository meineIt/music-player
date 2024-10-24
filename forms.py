from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, widgets, PasswordField, BooleanField
from wtforms_alchemy import QuerySelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo 


class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddPlaylistForm(FlaskForm):
    playlist_name_field = StringField('PLAYLIST NAME', validators=[DataRequired()])
    users_field = QuerySelectMultipleFieldWithCheckboxes("ADD THIS PLAYLIST TO:", validators=[DataRequired()])
    submit_field = SubmitField('ADD')


class AddSongForm(FlaskForm):
    artist_field = StringField('ARTIST', validators=[DataRequired()])
    title_field = StringField('TITLE', validators=[DataRequired()])
    url_field = StringField('URL', validators=[DataRequired()])
    grade_field = RadioField('GRADE', choices=[(1, "★"), (2,"★"), (3,"★"), (4,"★"), (5,"★")], validators=[DataRequired()])
    playlist_field = SelectField('ADD THIS SONG TO:', choices=[], validators=[DataRequired()])
    submit_field = SubmitField('ADD')


class DeleteForm(FlaskForm):
    delete_playlist_button = SubmitField('DELETE LIST')
    delete_song_button = SubmitField('DELETE SONG')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('LOG IN')
