from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_login import current_user

from socialchan.models import Usuario


class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired('Nombre de usuario requerido'), Length(min=3, max=12)])
    email = StringField('Correo Electronico', validators=[DataRequired('Nombre de usuario requerido'), Email('Direccion de correo invalido')])
    password = PasswordField('Contraseña', validators=[DataRequired('Se requiere una contraseña')])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas no coinciden')])
    submit = SubmitField('Registrar')


    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()

        if user:
            raise ValueError('Nombre de usuario ya existe!!')

    def validate_email(self, email):
        ema = Usuario.query.filter_by(email=email.data).first()

        if ema:
            raise ValueError('El correo electronico ya existe!!')


class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired('Nombre de usuario requerido'), Length(min=3, max=12)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordar usuario')
    submit = SubmitField('Ingresar')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired('Nombre de usuario requerido'), Length(min=3, max=12)])
    email = StringField('Correo Electronico', validators=[DataRequired('Nombre de usuario requerido'), Email('Direccion de correo invalido')])

    picture = FileField('Actualizar foto de perfil..', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Solo se permiten imagenes. jpg y png')])

    submit = SubmitField('Actualizar!!')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Usuario.query.filter_by(username=username.data).first()
            if user:
                raise ValueError('Nombre de usuario ya existe!!')

    def validate_email(self, email):
        if email.data != current_user.email:
            ema = Usuario.query.filter_by(email=email.data).first()

            if ema:
                raise ValueError('El correo electronico ya existe!!')