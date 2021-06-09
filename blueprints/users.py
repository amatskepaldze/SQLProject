# -*- coding: utf-8 -*-
import datetime
import os
from PIL import Image

from flask import (Flask, render_template, redirect, request, abort, Blueprint, current_app, url_for, flash)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
from werkzeug.utils import secure_filename

from data.db_session import global_init, create_session
from data.news import News
from data.users import User
from data.comments import Comments

from forms.user import LoginForm, RegisterForm, EditProfile, EditPasswordEmail, EditAvatar

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

blueprint_users = Blueprint(
    'blueprint_users',
    __name__,
    template_folder='templates',
    static_folder='static'
)


def crop_center(picture_path):  # Функция для обрезки изображения по центру.
    pil_img = Image.open(os.path.join(current_app.config['UPLOAD_FOLDER'], f"{picture_path}.png"))
    img_width, img_height = pil_img.size
    crop = min(pil_img.size)
    new_img = pil_img.crop(
        ((img_width - crop) // 2, (img_height - crop) // 2, (img_width + crop) // 2, (img_height + crop) // 2))
    new_img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], f"{picture_path}.png"))


def upload_avatar(file, user):  # db_sess.commit() after each call
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        user.delete_avatar()
        user.set_picture()
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], f"{user.picture_path}.png"))
        crop_center(user.picture_path)
        return True
    if file:
        flash('Неправильный формат файла')
    return False


def not_found_users(message='такого пользователя не существует'):
    return render_template('nothing.html', message=message, title='404')


@blueprint_users.route('/')
@login_required
def my_profile():
    return redirect(f'/user/{current_user.id}')


@blueprint_users.route('/<id>')
def profile(id):
    db_sess = create_session()
    if id.isdigit():
        user = db_sess.query(User).filter(User.id == int(id)).first()
    else:
        user = db_sess.query(User).filter(User.name == id).first()
    if not user:
        return not_found_users()
    return render_template('profile/profile.html', user=user, news=user.get_news(privat=current_user == user),
                           title=user.name)


@blueprint_users.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    db_sess = create_session()
    if form.validate_on_submit():
        same_name = db_sess.query(User).filter(User.name == form.name.data).first()
        if same_name and same_name.name != current_user.name:
            return render_template('profile/edit_profile.html', form=form,
                                   message="Такой пользователь уже есть", title='редактирование профиля')

        user = db_sess.query(User).filter(User.name == current_user.name).first()
        user.name = form.name.data
        user.about = form.about.data
        user.instrument = form.instrument.data

        # upload_avatar(file=form.file.data, user=user)

        db_sess.commit()
        return redirect('/user')
    form.name.data = current_user.name
    form.about.data = current_user.about
    form.instrument.data = current_user.instrument

    return render_template('profile/edit_profile.html', form=form, title='редактирование профиля')


@blueprint_users.route('/edit/avatar', methods=['GET', 'POST'])
@login_required
def edit_avatar():
    form = EditAvatar()
    if form.validate_on_submit():
        print(form.file.data)
        db_sess = create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        upload_avatar(file=form.file.data, user=user)
        db_sess.commit()
        return redirect('/user')
    return render_template('profile/edit_avatar.html', form=form, title='Изменить аватарку')


@blueprint_users.route('/edit/avatar/delete', methods=['POST', 'GET'])
@login_required
def edit_avatar_delete():
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.delete_avatar()
    db_sess.commit()
    return redirect('/user')


@blueprint_users.route('/redact', methods=['GET', 'POST'])
@login_required
def redact():
    form = EditPasswordEmail()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user or not user.check_password(form.password.data) or user != current_user:
            return render_template('profile/redact_profile.html',
                                   message="Неправильный логин или пароль",
                                   form=form, title='редактирование профиля')
        if form.new_password.data != form.new_password_again.data:
            return render_template('profile/redact_profile.html', title='редактирование профиля',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(
                User.email == form.new_email.data).first() and current_user.email != form.new_email.data:
            return render_template('profile/redact_profile.html', title='редактирование профиля',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user.email = form.new_email.data
        user.set_password(form.new_password.data)
        db_sess.commit()
        return redirect('/')
    return render_template('profile/redact_profile.html', title='редактирование профиля', form=form)


@blueprint_users.route('/<int:id>/liked_news', methods=['GET'])
@login_required
def liked_news(id):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    liked_news = list(map(lambda x: x.news, sorted(user.likes, key=lambda x: x.created_date, reverse=True)))
    return render_template('profile/liked_news.html', user=user, news=liked_news, title=f'понравилось {user.name}')
