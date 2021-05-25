# -*- coding: utf-8 -*-
import datetime
import os

from flask import (Flask, render_template, redirect, request, abort, Blueprint)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
from flask_restful import abort, Api

from data.db_session import global_init, create_session
from data.news import News
from data.users import User
from data.comments import Comments

from forms.news import NewsForm, Response
from forms.user import LoginForm, RegisterForm, EditProfile, EditPasswordEmail

blueprint_users = Blueprint(
    'blueprint_users',
    __name__,
    template_folder='templates',
    static_folder='static'
)


def not_found_users(message='такого пользователя не существует'):
    return render_template('nothing.html', message=message)


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
    return render_template('profile/profile.html', user=user, news=user.get_news(privat=current_user == user))


@blueprint_users.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    db_sess = create_session()
    if form.validate_on_submit():
        same_name = db_sess.query(User).filter(User.name == form.name.data).first()
        if same_name and same_name.name != current_user.name:
            return render_template('profile/edit_profile.html', form=form,
                                   message="Такой пользователь уже есть")

        user = db_sess.query(User).filter(User.name == current_user.name).first()
        user.name = form.name.data
        user.about = form.about.data
        user.instrument = form.instrument.data
        db_sess.commit()
        return redirect('/user')
    form.name.data = current_user.name
    form.about.data = current_user.about
    form.instrument.data = current_user.instrument

    return render_template('profile/edit_profile.html', form=form)


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
                                   form=form)
        if form.new_password.data != form.new_password_again.data:
            return render_template('profile/redact_profile.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(
                User.email == form.new_email.data).first() and current_user.email != form.new_email.data:
            return render_template('profile/redact_profile.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user.email = form.new_email.data
        user.set_password(form.new_password.data)
        db_sess.commit()
        return redirect('/')
    return render_template('profile/redact_profile.html', title='Регистрация', form=form)
