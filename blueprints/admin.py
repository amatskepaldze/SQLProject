# -*- coding: utf-8 -*-
import datetime
import os
from functools import wraps

from flask import (Flask, render_template, redirect, request, abort, Blueprint)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)

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


@blueprint_admin.route('/tables/likes', methods=['GET'])  # удаление комментария
@login_required
@admin
def admin_likes():
    db_sess = create_session()
    likes = db_sess.query(Likes)
    return render_template('admin/likes.html', title='likes', likes=likes)


@blueprint_admin.route('/tables/likes/<int:id>', methods=['GET'])  # удаление комментария
@login_required
@admin
def rm_like(id):
    db_sess = create_session()
    like = db_sess.query(Likes).filter(Likes.id == id).first()
    if like:
        try:
            like.delete()
        except:
            print(like)
        db_sess.delete(like)
        db_sess.commit()
        return redirect('/admin/tables/likes')
    return 'not found'
