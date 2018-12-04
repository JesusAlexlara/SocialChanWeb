import secrets
import os
import markdown2
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Markup
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
    boards = Board.query.all()
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
    return render_template('register.html', title='Registro', form=form, boards=boards)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    boards = Board.query.all()
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
    return render_template('login.html', title='Ingreso', form=form, boards=boards)


@app.route('/')
@app.route('/home')
def home():
    boards = Board.query.all()
    threads = Thread.query.order_by(Thread.date_posted).limit(5).all()
    return render_template('home.html', title="inicio", boards=boards, posts=posts, threads=threads)


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

##################Tableros#################################################
@app.route('/board', methods=['GET', 'POST'])
@login_required
def board():
    form = BoardForm()

    if form.validate_on_submit():
        board = Board(
            title=form.title.data,
            short_title=form.short_title.data,
            registered_user=form.registrados.data,
            Description=form.descripcion.data
        )
        db.session.add(board)
        db.session.commit()
        flash('Se guardo el tablon satisfactoriamente', 'success')
        return redirect(url_for('board'))
    return render_template('board.html', title='Tableros', form=form)


@app.route('/<name>/edit', methods=['GET', 'POST'])
@login_required
def update_board(name):
    form = BoardFormEdit()
    board = Board.query.filter_by(short_title=name).first()
    if board:
        if form.validate_on_submit():

            board.title = form.title.data
            board.short_title = form.short_title.data
            board.registered_user = form.registrados.data,
            board.Description = form.descripcion.data

            db.session.commit()
            flash('Se edito el tablon satisfactoriamente', 'success')
            return redirect(url_for('board'))
        elif request.method == 'GET':
            form.title.data = board.title
            form.short_title.data = board.short_title
            form.registrados.data = board.registered_user
            form.descripcion.data = board.Description
        return render_template('board_edit.html', title='Tableros', form=form)
    flash('No existe el tablero', 'danger')
    return redirect(url_for('home'))




@app.route('/<name>/del', methods=['GET', 'POST'])
@login_required
def delete_board(name):
    board = Board.query.filter_by(short_title=name).first()
    if board:
        db.session.delete(board)
        db.session.commit()
        flash('Se elimino el tablero', 'success')
        return redirect(url_for('home'))
    flash('No existe el tablero', 'danger')
    return redirect(url_for('home'))


############################################################################


@app.route('/<name>')
def layaout(name):
    #Verificacion de solo usuarios registrados
    board = Board.query.filter_by(short_title=name).first()
    if not board:
        flash('No tienes permisos o no existe este elemento', 'danger')
        return redirect(url_for('home'))
    boards = Board.query.all()
    page = request.args.get('page', 1, type=int)
    threads = Thread.query.paginate(page=page, per_page=5)
    return render_template('layaout.html', title='Tableros', board=board, boards=boards, threads=threads, page=page)


@app.route('/<name>/new', methods=['GET', 'POST'])
def create_Thread(name):
    board = Board.query.filter_by(short_title=name).first()
    form = ThreadForm()
    if not board:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    if form.validate_on_submit():
        # user = Usuario.query.filter_by(id=current_user.id).first()
        mk = markdown2.markdown(form.contenido.data)
        sec = secrets.token_hex(5)
        thread = Thread(
            title=form.title.data,
            content=mk,
            raw_content=form.contenido.data,
            code=sec,
            registered=form.registrados.data,
            tablero=board,
            usuario=current_user
        )
        db.session.add(thread)
        db.session.commit()
        flash(f'Se guardo el hilo satisfactoriamente /{ sec }', 'success')
        return redirect(url_for('home'))
    return render_template('createThread.html', title='Nuevo hilo :D', form=form)


@app.route('/<name>/<hilo>', methods=['GET', 'POST'])
def hilo(name, hilo):
    board = Board.query.filter_by(short_title=name).first()
    if not board:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    hilox = Thread.query.filter_by(code=hilo).first()
    if not hilox:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))

    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.contenido.data,
            hilo=hilox,
            usuario=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Se creo el post', 'success')
        return redirect(url_for('hilo', name=name, hilo=hilo))
    boards = Board.query.all()
    return render_template('hilo.html', form=form, title=hilo.title, thread=hilox, boards=boards)


@app.route('/<name>/<hilo>/del')
def eliminar_hilo(name, hilo):
    board = Board.query.filter_by(short_title=name).first()
    if not board:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    hilo = Thread.query.filter_by(code=hilo).first()
    if not hilo:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    if not current_user.id == hilo.user_id:
        flash('No eres el duelo del hilo :P', 'danger')
        return redirect(url_for('hilo', name=name, hilo=hilo))
    db.session.delete(hilo)
    db.session.commit()
    flash('Se elimino el hilo exitosamente', 'success')
    return redirect(url_for('layaout', name=name))


@app.route('/<name>/<hilo>/mod', methods=['GET', 'POST'])
def modificar_hilo(name, hilo):
    board = Board.query.filter_by(short_title=name).first()
    if not board:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    hilox = Thread.query.filter_by(code=hilo).first()
    if not hilox:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    if not current_user.id == hilox.user_id:
        flash('No eres el duelo del hilo :P', 'danger')
        return redirect(url_for('hilo', name=name, hilo=hilo))
    form = ModThreadForm()
    if form.validate_on_submit():
        hilox.title = form.title.data
        hilox.raw_content = form.contenido.data
        hilox.content = markdown2.markdown(form.contenido.data)
        hilox.registered = form.registrados.data
        db.session.commit()
        return redirect(url_for('hilo', name=name, hilo=hilo))
    elif request.method == 'GET':
        form.title.data = hilox.title
        form.contenido.data = hilox.raw_content
        form.registrados.data = hilox.registered

    return render_template('mod_hilo.html', title='modificar hilo :D', form=form)


@app.route('/<name>/<hilo>/<id>/comment', methods=['GET', 'POST'])
def comentar(name, hilo, id):
    board = Board.query.filter_by(short_title=name).first()
    if not board:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    hilox = Thread.query.filter_by(code=hilo).first()
    if not hilox:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    poste = Post.query.filter_by(id=id).first()
    if not poste:
        flash('accion no permitida', 'danger')
        return redirect(url_for('home'))
    form = CommentForm()
    if form.validate_on_submit():
        cm = Comments(
            content=form.scontenido.data,
            usuario=current_user,
            post=poste
        )
        db.session.add(cm)
        db.session.commit()

        flash('Se guardo el cometario', 'success')
        return redirect(url_for('hilo', name=name, hilo=hilo))
    return render_template('comment.html', form=form, title="comentar")