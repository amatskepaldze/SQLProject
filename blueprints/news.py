# -*- coding: utf-8 -*-
import datetime
import os

from flask import (Flask, render_template, redirect, request, abort, Blueprint)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)

from data.db_session import global_init, create_session
from data.news import News
from data.users import User
from data.comments import Comments
from data.likes import Likes

from forms.news import NewsForm
from forms.comments import CommentsForm

blueprint_news = Blueprint(
    'blueprint_news',
    __name__,
    template_folder='templates',
    static_folder='static'
)


def not_found_news(message='такой новости нет'):
    return render_template('nothing.html', message=message, title='404')


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
    return render_template('news/edit_news.html', title='Добавление новости', form=form, action="Добавление новости")


@blueprint_news.route('/<int:id>', methods=['GET', 'POST'])  # просмотр новости
def news(id):
    db_sess = create_session()
    ns = db_sess.query(News).filter(News.id == id).first()
    if not ns:
        return not_found_news()
    if ns.is_private and ns.user_id != current_user.id:
        return abort(405)

    form = CommentsForm()
    if form.validate_on_submit():
        comment = Comments(comment=form.comment.data, news_id=ns.id, user_id=current_user.id,
                           is_private=form.is_private.data, news=ns)
        db_sess.add(comment)
        comment.post()
        db_sess.commit()
        return redirect(f'/news/{id}')
    comments = ns.get_comments(privat=current_user == ns.user)
    return render_template('news/news.html', title=ns.title, item=ns, comments=comments, form=form,
                           liked=any(filter(lambda x: x.user == current_user, ns.likes)))


@blueprint_news.route('/edit/<int:id>', methods=['GET', 'POST'])  # изменение новости
@login_required
def edit_news(id):
    db_sess = create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if not news:
        abort(404)

    form = NewsForm()
    if request.method == "GET":
        form.title.data = news.title
        form.content.data = news.content
        form.is_private.data = news.is_private

    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        db_sess.commit()
        return redirect('/')
    return render_template('news/edit_news.html', title='Редактирование новости', form=form, action="Изменение новости")


@blueprint_news.route('/<int:id>/like', methods=['POST'])
def like_the_news(id):
    if not current_user.is_authenticated:
        return abort(405)
    db_sess = create_session()
    ns = db_sess.query(News).filter(News.id == id).first()
    if not ns or ns.user == current_user:
        return abort(404)
    like = db_sess.query(Likes).filter(Likes.user == current_user and Likes.news == ns).first()
    print(f"ns:{ns.id} lk:{like.id} ")
    if like:
        like.delete()
        db_sess.delete(like)
    else:
        like = Likes(user_id=current_user.id, news_id=ns.id, news=ns)
        db_sess.add(like)
        db_sess.commit()
        like.post()
    db_sess.commit()
    return redirect(f'/news/{id}')