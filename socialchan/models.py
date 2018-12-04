from datetime import datetime as dt
from socialchan import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

#Definición de los modelos de la Base de datos
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    avatar_file = db.Column(db.String(50), nullable=False, default='avatar.png')
    is_admin = db.Column(db.Boolean, default=False)

    thread = db.relationship('Thread', backref='usuario', lazy=True)
    posts = db.relationship('Post', backref='usuario', lazy=True)
    comments = db.relationship('Comments', backref='usuario', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar_file}')"


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    short_title = db.Column(db.String(3), nullable=False)
    registered_user = db.Column(db.Boolean)
    Description = db.Column(db.Text, nullable=False)

    threads = db.relationship('Thread', backref='tablero', lazy=True)

    def __repr__(self):
        return f"Board('{self.title}', {self.short_title})"


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    raw_content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    code = db.Column(db.String(4), unique=False, nullable=True)
    registered = db.Column(db.Boolean)

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    posts = db.relationship('Post', backref='hilo', lazy=True, cascade = "all,delete")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    content = db.Column(db.Text, nullable=False)
    raw_content = db.Column(db.Text, nullable=False)

    comments = db.relationship('Comments', backref='post', lazy=True)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=dt.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


#
# class Category(db.Model):
#     pass