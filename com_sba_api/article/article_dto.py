from com_sba_api.ext.db import db
from com_sba_api.user import User
from com_sba_api.item import Item

class Article(Base):
    __tablename__ = "articles"
    __table_args__={'mysql_collate':'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    item_id = db.Column(db.Integer, db.ForeignKey(Item.id))
    title = db.Column(db.String)
    content = db.Column(db.String)

    def __repr__(self):
        return f'id={self.id}, user_id={self.user_id}, item_id={self.item_id},\
            title={self.title}, content={self.content}'

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id' : self.item_id,
            'title' : self.title,
            'content' : self.content
        }

class ArticleDto(object):
    id: int
    user_id: int
    item_id: int
    title: str
    content: str

