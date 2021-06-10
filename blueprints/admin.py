# -*- coding: utf-8 -*-
import datetime
import os
from functools import wraps

from flask import (Flask, render_template, redirect, request, abort, Blueprint)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
from flask_restful import reqparse

from data.db_session import global_init, create_session
from data.news import News
from data.users import User
from data.comments import Comments
from data.likes import Likes

from forms.comments import CommentsForm

blueprint_admin = Blueprint(
    'blueprint_admin',
    __name__,
    template_folder='templates'
)


def admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.id == 1:
            return func(*args, **kwargs)
        return abort(405)

    return wrapper


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int)
parser.add_argument('news_id', type=int)
parser.add_argument('id', type=int)


@blueprint_admin.route('/tables/news', methods=['GET'])
@login_required
@admin
def admin_news():
    args = parser.parse_args()
    db_sess = create_session()
    news = db_sess.query(News)
    if not args.get('user_id') is None:
        news = news.filter(News.user_id == args.get('user_id'))
    return render_template('admin/tables/news.html', title='news', news=news)


@blueprint_admin.route('/tables/likes', methods=['GET'])
@login_required
@admin
def admin_likes():
    args = parser.parse_args()
    db_sess = create_session()
    likes = db_sess.query(Likes)
    if not args.get('user_id') is None:
        likes = likes.filter(Likes.user_id == args.get('user_id'))
    elif not args.get('news_id') is None:
        likes = likes.filter(Likes.news_id == args.get('news_id'))
    return render_template('admin/tables/likes.html', title='likes', likes=likes)


@blueprint_admin.route('/tables/comments', methods=['GET'])
@login_required
@admin
def admin_comments():
    args = parser.parse_args()
    db_sess = create_session()
    comments = db_sess.query(Comments)
    if not args.get('user_id') is None:
        comments = comments.filter(Comments.user_id == args.get('user_id'))
    elif not args.get('news_id') is None:
        comments = comments.filter(Comments.news_id == args.get('news_id'))
    return render_template('admin/tables/comments.html', title='comments', comments=comments)


@blueprint_admin.route('/tables/users', methods=['GET'])
@login_required
@admin
def admin_users():
    db_sess = create_session()
    users = db_sess.query(User)
    return render_template('admin/tables/users.html', title='users', users=users)


@blueprint_admin.route('/tables/<string:inst>/delete/<int:id>', methods=['GET'])  # удаление
@login_required
@admin
def rm_obj(inst, id):
    db_sess = create_session()
    class_obj = {'likes': Likes, 'comments': Comments, 'news': News}.get(inst)
    obj = db_sess.query(class_obj).filter(class_obj.id == id).first()
    if obj:
        try:
            obj.delete(db_sess)
        except:
            print(obj)
        db_sess.delete(obj)
        db_sess.commit()
        return redirect(f'/admin/tables/{inst}')
    return 'not found'


@blueprint_admin.route('/tables/users/delete_avatar/<int:id>', methods=['GET'])  # удаление
@login_required
@admin
def rm_avatar(id):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        try:
            user.delete_avatar()
        except:
            return f'cannot {id}'
        db_sess.commit()
        return redirect(f'/admin/tables/users')
    return 'not found'
