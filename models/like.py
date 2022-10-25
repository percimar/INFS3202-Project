from sqlalchemy import Column, ForeignKey

from db import db, table_name_prefix, table_name_prefix_with_schema


class Like(db.Model):
    __tablename__ = table_name_prefix + "likes"
    __table_args__ = {"schema": "public"}  # needed for db.drop_all() to work https://stackoverflow.com/a/56499548

    user_id = Column(ForeignKey(table_name_prefix_with_schema + 'users.id'), primary_key=True)
    post_id = Column(ForeignKey(table_name_prefix_with_schema + 'posts.id'), primary_key=True)

    @classmethod
    def get_record(cls, user_id, post_id):
        return cls.query.filterBy(user_id=user_id, post_id=post_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True
