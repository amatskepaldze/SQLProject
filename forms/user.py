from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    file = FileField('Аватарка')
    about = TextAreaField("Немного о себе")
    instrument = StringField('Инструмент')
    submit = SubmitField('Войти')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditProfile(FlaskForm):
    name = StringField('Имя пользователя')
    about = TextAreaField("О себе")
    instrument = StringField('Инструмент')
    submit = SubmitField('Изменить')


class EditPasswordEmail(FlaskForm):
    email = EmailField('Старая почта', validators=[DataRequired()])
    password = PasswordField('Старый пароль', validators=[DataRequired()])

    new_email = EmailField('Новая почта', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    new_password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Редактировать')
