import datetime
import sqlalchemy
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
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

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

    def __repr__(self):
        return f"<{self.__tablename__}>\t{self.name}\t{self.email}"
