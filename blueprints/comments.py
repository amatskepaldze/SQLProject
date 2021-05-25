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

from forms.comments import CommentsForm

blueprint_comments = Blueprint(
    'blueprint_comments',
    __name__,
    template_folder='templates'
)


def not_found_news(message='такого коментария нет'):
    return render_template('nothing.html', message=message)


@blueprint_comments.route('/delete/<int:id>', methods=['GET'])  # удаление комментария
@login_required
def comm_delete(id):
    db_sess = create_session()
    cm = db_sess.query(Comments).filter(Comments.id == id).first()
    if cm:
        if current_user.id != cm.user_id:
            abort(405)
        cm.delete()
        db_sess.delete(cm)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/news/{cm.news_id}')


@blueprint_comments.route('/edit/<int:id>', methods=['GET', 'POST'])  # изменение новости
@login_required
def edit_comm(id):
    db_sess = create_session()
    comm = db_sess.query(Comments).filter(Comments.id == id, Comments.user == current_user).first()
    if not comm:
        abort(404)

    form = CommentsForm()

    if request.method == "GET":
        form.comment.data = comm.comment
        form.is_private.data = comm.is_private

    if form.validate_on_submit():
        comm.comment = form.comment.data
        comm.is_private = form.is_private.data
        db_sess.commit()
        return redirect(f'/news/{comm.news_id}')
    return render_template('comments/comments.html', form=form, title='Редактирование комментария',
                           news=[comm.news])
