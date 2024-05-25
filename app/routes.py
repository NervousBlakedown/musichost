# Route to handle file uploads and save them to server.
# Imports
import os
from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import RegistrationForm, LoginForm, UploadForm
from app.models import User, Song
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    songs = Song.query.all()
    return render_template('index.html', songs=songs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

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
        flash('Your song has been uploaded!', 'success')
        return redirect(url_for('home'))
    return render_template('upload.html', title='Upload Music', form=form)

