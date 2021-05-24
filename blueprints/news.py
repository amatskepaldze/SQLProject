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
from forms.user import LoginForm, RegisterForm, EditProfile

blueprint_news = Blueprint(
    'blueprint_news',
    __name__,
    template_folder='templates',
    static_folder='static'
)


def not_found_news(message='такой новости нет'):
    return render_template('nothing.html', message=message)


@blueprint_news.route('/delete/<int:id>', methods=['GET'])  # удаление новости
@login_required
def news_delete(id):
    db_sess = create_session()
    ns = db_sess.query(News).filter(News.id == id).first()
    if ns:
        if current_user.id != ns.user_id:
            abort(405)
        db_sess.delete(ns)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@blueprint_news.route('/', methods=['GET', 'POST'])  # создание новости
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('edit_news.html', title='Добавление новости', form=form)


@blueprint_news.route('/<int:id>', methods=['GET', 'POST'])  # просмотр новости
def news(id):
    db_sess = create_session()
    ns = db_sess.query(News).filter(News.id == id).first()
    if not ns:
        return not_found_news()
    if ns.is_private and ns.user_id != current_user.id:
        return abort(405)

    form = Response()
    if form.validate_on_submit():
        comment = Comments(comment=form.comment.data, news_id=ns.id, user_id=current_user.id,
                           is_private=form.is_private.data, news=ns)
        db_sess.add(comment)
        comment.post()
        db_sess.commit()
        return redirect(f'/news/{id}')
    comments = ns.get_comments(privat=current_user == ns.user)
    return render_template('news.html', title=ns.title, item=ns, comments=comments, form=form)


@blueprint_news.route('/edit/<int:id>', methods=['GET', 'POST'])  # изменение новости
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit_news.html', title='Редактирование новости', form=form)
