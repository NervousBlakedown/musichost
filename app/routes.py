# Route to handle file uploads and save them to server.
# Imports
import os
from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import UploadForm
from app.models import Song
from flask_login import current_user, login_required

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.root_path, 'static/music', filename)
        file.save(file_path)
        song = Song(title=filename, file_path=file_path, author=current_user)
        db.session.add(song)
        db.session.commit()
        flash('Your song has been uploaded.', 'success')
        return redirect(url_for('home'))
    return render_template('upload.html', title='Upload Music', form=form)
