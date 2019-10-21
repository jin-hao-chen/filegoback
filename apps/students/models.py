# -*- coding: utf-8 -*-
from apps import db


class Student(db.Model):

    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sid = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(32), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, sid, name, is_admin=False):
        self.sid = sid
        self.name = name
        self.is_admin = is_admin

    def __str__(self):
        return "<Student '%s'>" % self.sid

    def __repr__(self):
        return str(self)
