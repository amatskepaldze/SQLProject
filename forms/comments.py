from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class CommentsForm(FlaskForm):
    comment = TextAreaField("Написать коментарий:", validators=[DataRequired()])
    is_private = BooleanField("Лично автору")
    submit = SubmitField('Отправить')


class EditCommentsForm(FlaskForm):
    comment = TextAreaField("Коментарий", validators=[DataRequired()])
    is_private = BooleanField("Лично автору")
    submit = SubmitField('Изменить')
