import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from socialchan import app, db, bcrypt

from socialchan.forms import *
from socialchan.models import *


posts = [
    {
        'author': 'el yeyo',
        'title': 'Blog de LoL',
        'content': 'Como no ser un manco',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Chuyetas',
        'title': 'Blog de dios',
        'content': 'Yoloasd',
        'date_posted': 'April 21, 2018'
    }
]


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Usuario(username=form.username.data, email=form.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        message = f'Se creo la cuenta { form.username.data } puedes iniciar sesión!!'
        flash(message , 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registro', form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Datos incorrectos, verifica nombre de usuario y contraseña.', 'danger')
    return render_template('login.html', title='Ingreso', form=form)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="inicio", posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def guarda_imagen(imagen):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(imagen.filename)
    dir = random_hex + ext
    dir_final = os.path.join(app.root_path, 'static/img/avatars', dir)

    tam = (125, 125)
    i = Image.open(imagen)
    i.thumbnail(tam)

    i.save(dir_final)
    return dir


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            file = guarda_imagen(form.picture.data)
            current_user.avatar_file = file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tu cuenta ha sido actualizada!!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Perfil', form=form)

