# coding=utf-8
from extensions import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    selected_calendar_group = db.Column(db.String(256))
    token = db.Column(db.String(512))

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def tojson(self):
        return self.columnitems


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    subject = db.Column(db.String(128))
    sdate = db.Column(db.DateTime)
    edate = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    group = db.Column(db.String)
    birthday = db.Column(db.String)

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def tojson(self):
        return self.columnitems


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    creator_email = db.Column(db.String)

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def tojson(self):
        return self.columnitems
