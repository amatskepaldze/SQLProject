from datetime import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class NewsRelation(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news_relation'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    news_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("news.id"))

    created_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    comment = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('User')
    news = orm.relation('News')


