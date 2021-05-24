import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    picture_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    reacted_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    user = orm.relation('User')
    comments = orm.relation('Comments', back_populates='news')

    def short_content(self, length=60):
        return self.content.rjust(length, ' ')[:length]

    def __repr__(self):
        return f"<{self.__tablename__}>[{self.user}]\t{self.title}\t({self.created_date})\tpriv:{self.is_private}"

    def get_comments(self, privat=False):
        return sorted(filter(lambda x: not x.is_private or privat, self.comments), key=lambda x: x.created_data)
