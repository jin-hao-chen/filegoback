# -*- coding: utf-8 -*-

from apps.files.models import File
from apps.students.models import Student
from apps import utils


def send_msg_when_upload_new_file(sender, sid, file):
    subject = (Student.query.filter_by(sid=sid).first().name + "上传了文件 '%s' ") % file.filename
    remain = len(Student.query.all()) - len(File.query.all())
    msg = sender.make_msg(subject, date=utils.get_datetime(), content="""
            %s
            还有 %s 个人没有上交
            """ % (subject, remain))
    sender.send(msg)


def send_msg_when_replace_file(sender, sid, file):
    subject = (Student.query.filter_by(sid=sid).first().name + "重新上传了文件 '%s' ") % file.filename
    remain = len(Student.query.all()) - len(File.query.all())
    msg = sender.make_msg(subject, date=utils.get_datetime(), content="""
                %s
                还有 %s 个人没有上交
                """ % (subject, remain))
    sender.send(msg)


def send_msg_when_delete_file(sender, sid, file):
    subject = (Student.query.filter_by(sid=sid).first().name + "删除了文件 '%s' ") % file.filename
    remain = len(Student.query.all()) - len(File.query.all())
    msg = sender.make_msg(subject, date=utils.get_datetime(), content="""
            %s
            还有 %s 个人没有上交
            """ % (subject, remain))
    sender.send(msg)