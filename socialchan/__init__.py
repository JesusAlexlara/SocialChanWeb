from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'p&V11t=__KY$X)&?(nvBLz=|tp(n?V'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialchan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Necesitar estar logeado!!!'
login_manager.login_message_category = 'danger'


from socialchan import routes