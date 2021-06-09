import datetime
import sqlalchemy
import os
from random import randint
from flask import current_app
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    instrument = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    picture_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    # last_read_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    news = orm.relation("News", back_populates='user')
    comments = orm.relation('Comments', back_populates='user')
    likes = orm.relation("Likes", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_news(self, privat=False):
        return sorted(filter(lambda x: (not x.is_private or privat), self.news), key=lambda x: x.created_date,
                      reverse=True)

    def set_picture(self):
        self.picture_path = str(randint(10000, 100000))

    def get_picture_path(self):
        name = f"{self.picture_path}.png" if self.picture_path else 'default.png'
        return '/static/avatars/' + name

    def delete_avatar(self):  # need db_sess.commit
        if self.picture_path:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], f"{self.picture_path}.png"))
            self.picture_path = None

    def get_short_time(self):
        return self.created_date.strftime('%d %b %H:%M')

    def __repr__(self):
        return f"<{self.__tablename__}>\t{self.name}\t{self.email}"
