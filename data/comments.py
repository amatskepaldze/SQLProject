from datetime import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Comments(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    news_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("news.id"))

    created_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=True)

    comment = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user = orm.relation('User')
    news = orm.relation('News')

    def short_content(self, length=60):
        return self.comment.rjust(length, ' ')[:length]

    def post(self):
        self.news.reacted_count += 1

    def delete(self, db_sess=None):
        self.news.reacted_count -= 1

    def get_short_time(self):
        return self.created_data.strftime('%d %b %H:%M')
