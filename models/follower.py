from sqlalchemy import Column, ForeignKey

from db import db, table_name_prefix_with_schema, table_name_prefix


class Follower(db.Model):
    __tablename__ = table_name_prefix + "followers"
    __table_args__ = {"schema": "public"}  # needed for db.drop_all() to work https://stackoverflow.com/a/56499548

    user_id = Column(ForeignKey(table_name_prefix_with_schema + 'users.id'), primary_key=True)
    following_id = Column(ForeignKey(table_name_prefix_with_schema + 'users.id'), primary_key=True)

    @classmethod
    def get_record(cls, user_id, following_id):
        return cls.query.filter_by(user_id=user_id, following_id=following_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True
