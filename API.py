from flask_restful import reqparse, abort, Api, Resource
from flask import (Flask, )
import datetime


app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
