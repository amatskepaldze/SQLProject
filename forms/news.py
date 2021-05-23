from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')


class Response(FlaskForm):
    comment = TextAreaField("Коментарий", validators=[DataRequired()])
    is_private = BooleanField("Лично автору")
    submit = SubmitField('Отправить')
