from datetime import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Likes(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    news_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("news.id"))

    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    user = orm.relation('User')
    news = orm.relation('News')

    def post(self):
        self.news.likes_count += 1

    def delete(self, db_sess=None):
        self.news.likes_count -= 1

    def get_short_time(self):
        return self.created_date.strftime('%d %b %H:%M')

    def __repr__(self):
        return f"id:{self.id} user_id:{self.user_id} news_id:{self.news_id} created_date:{self.created_date}"
