import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    picture_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    reacted_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    user = orm.relation('User')
    reactions = orm.relation('NewsRelation', back_populates='news')

    def short_content(self, length=50):
        return self.content.rjust(length, ' ')[:length]

    def __repr__(self):
        return f"<{self.__tablename__}>[{self.user}]\t{self.title}\t({self.created_date})\tpriv:{self.is_private}"
