# Form to handle .mp3 file uploads.
# Imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadForm(FlaskForm):
    file = FileField('Upload Music', validators=[
        FileRequired(),
        FileAllowed(['mp3'], 'MP3 files only!')
    ])
    submit = SubmitField('Upload')
