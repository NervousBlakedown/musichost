from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, db, Music
from .forms import LoginForm, RegisterForm

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = f'static/music/{filename}'
            file.save(filepath)
            new_music = Music(title=title, filename=filename, user_id=current_user.id)
            db.session.add(new_music)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('upload.html')

@main.route('/')
@login_required
def index():
    music_list = Music.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', music_list=music_list)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
