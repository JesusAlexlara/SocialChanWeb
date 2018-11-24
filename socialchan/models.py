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
    # posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar_file}')"


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(120), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"

#
#
# class Thread(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50), unique=True, nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
#     code = db.Column(db.String(4), unique=False, nullable=True)
#     registered = db.Column(db.Boolean)



# class Board(db.Model):
#     pass
#
#
# class Comments(db.Model):
#     pass
#
# class Category(db.Model):
#     pass