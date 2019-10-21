# -*- coding: utf-8 -*-
import datetime
from apps import db


class Category(db.Model):


    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    is_current = db.Column(db.Boolean, default=False)
    expire_time = db.Column(db.DateTime, nullable=False)


class File(db.Model):

    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(80), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.datetime.now)
    size = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    sid = db.Column(db.String(10), db.ForeignKey('student.sid'))
    owner = db.relationship('Student', uselist=False, backref=db.backref('file'))

    def __init__(self, sid, filename, upload_time, size, category_id):
        self.sid = sid
        self.filename = filename
        self.upload_time = upload_time
        self.size = size
        self.category_id = category_id

    def __str__(self):
        return 'File(sid=%s, filename=%s, upload_time=%s, size=%s, category_id=%s)'\
               % (self.sid, self.filename, self.upload_time, self.size, self.category_id)

    def __repr__(self):
        return str(self)
