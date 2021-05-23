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

blueprint_comments = Blueprint(
    'blueprint_comments',
    __name__,
    template_folder='templates'
)


def not_found_news(message='такой коментария нет'):
    return render_template('nothing.html', message=message)
