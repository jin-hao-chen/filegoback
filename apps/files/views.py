import os
import datetime
from flask import Blueprint
from flask.views import MethodView
from flask import (request, jsonify,
                   send_from_directory)
import settings
from apps import db
from apps.files.models import (File, Category)
from apps.students.models import Student
from apps.files import decorators
from apps import utils
from apps import config
from apps.files import tools
from libs import email_sender

sender = email_sender.EmailSender(sender='name',
                                  password='password',
                                  receiver='name@xxx.com')
files_bp = Blueprint('files', __name__)


def file_retrieve(sid):
    ret = {
        'code': config.CODE_OK
    }
    conditions = {
        'sid': sid
    }
    data = utils.jsonify_item_by(File, conditions)
    ret['item'] = data['item']
    ret['code'] = data['code']
    return ret


def file_download_file(sid):
    ret = file_retrieve(sid)
    if ret['code'] != config.CODE_OK:
        return ret
    file = ret['item']
    data = utils.jsonify_item_by(Category, {
        'id': file['category_id']
    })
    # ret = send_from_directory(os.path.join(settings.UPLOAD_DIR, data['item']['name']),
    #                           file['filename'],
    #                           as_attachment=True)
    # ret.headers['Content-Disposition'] = "attachment; filename*=utf-8''%s" % (file['filename'])
    ret['item'] = data['item']
    return ret


@decorators.add_owners_info
def file_list_all():
    ret = {
        'code': config.CODE_OK
    }
    items = File.query.all()
    data = utils.jsonify_items(items)
    ret['items'] = data['items']
    ret['code'] = data['code']
    return ret


@decorators.add_owners_info
def file_list_by(args):
    ret = {
        'code': config.CODE_OK
    }
    data = utils.jsonify_items_by(File, args)
    ret['items'] = data['items']
    ret['code'] = data['code']
    return ret


@decorators.add_owner_info
def file_create_new_file(file):
    ret = {
        'code': config.CODE_OK
    }
    sid = utils.fetch_sid(file.filename)
    conditions = {
        'sid': sid
    }
    data = utils.jsonify_item_by(Student, conditions)
    # If student with sid doesn't exist, return 1
    if data['code'] != config.CODE_OK:
        ret['code'] = config.CODE_ERROR
        return ret

    data = utils.jsonify_item_by(File, conditions)
    # This student never upload a file before
    if data['code'] != config.CODE_OK:
        current_category = Category.query.filter_by(is_current=True).first()
        doc = File(sid=sid,
                   filename=file.filename,
                   upload_time=datetime.datetime.now(),
                   size=0, # Will modify later
                   category_id=current_category.id)  # Will modify later
        db.session.add(doc)
        db.session.commit()
        directory = os.path.join(settings.UPLOAD_DIR, current_category.name)
        if not os.path.exists(directory):
            os.mkdir(directory)
        path = os.path.join(directory, doc.filename)
        file.save(path)
        ret['code'] = config.CODE_OK
        ret['item'] = utils.serialize(doc)

        tools.send_msg_when_upload_new_file(sender, sid, file)
        return ret

    # This student replace old file with a new file
    # Remove old file
    item = data['item']
    category = Category.query.filter_by(id=item['category_id']).first()
    old_path = os.path.join(settings.UPLOAD_DIR, category.name, item['filename'])
    os.remove(old_path)

    # Create new file
    new_path = os.path.join(settings.UPLOAD_DIR, category.name, file.filename)
    file.save(new_path)

    # Update file in table
    old_file = File.query.filter_by(sid=sid).first()
    old_file.filename = file.filename
    old_file.upload_time = datetime.datetime.now()

    db.session.commit()

    data = utils.jsonify_item_by(File, conditions)
    ret['code'] = data['code']
    ret['item'] = data['item']

    tools.send_msg_when_replace_file(sender, sid, file)
    return ret


@decorators.add_owner_info
def file_delete_existing_file(sid):
    ret = {
        'code': config.CODE_OK
    }
    conditions = {
        'sid': sid
    }
    data = utils.jsonify_item_by(File, conditions)
    if data['code'] != config.CODE_OK:
        ret['code'] = config.CODE_ERROR
        return ret
    file = File.query.filter_by(**conditions).first()
    db.session.delete(file)
    category = Category.query.filter_by(id=file.category_id).first()
    path = os.path.join(settings.UPLOAD_DIR, category.name, file.filename)
    os.remove(path)
    db.session.commit()
    ret['item'] = data['item']
    tools.send_msg_when_delete_file(sender, sid, file)
    return ret


@decorators.add_owner_info
def file_update_file(sid):
    ret = {
        'code': config.CODE_OK
    }
    file = File.query.filter_by(sid=sid).first()
    if file is None:
        ret['code'] = config.CODE_ERROR
        return ret
    for name in request.form:
        setattr(file, name, request.form.get(name))
    db.session.commit()
    ret['item'] = utils.jsonify_item_by(File, {'sid':sid})['item']
    return ret


class FileView(MethodView):

    methods = ['GET', 'POST', 'DELETE', 'PUT']

    def get(self, sid=None):
        if sid:
            if request.args.get('is_download'):
                return file_download_file(sid)
            return jsonify(**file_retrieve(sid))
        if not request.args:
            return jsonify(**file_list_all())
        return jsonify(**file_list_by(request.args))

    def post(self):
        file = request.files.get('file')
        if file:
            return jsonify(**file_create_new_file(file))
        ret = {
            'code': config.CODE_OK
        }
        return jsonify(**ret)

    def delete(self, sid=None):
        if sid:
            return jsonify(**file_delete_existing_file(sid))
        ret = {
            'code': config.CODE_ERROR02
        }
        return jsonify(**ret)

    def put(self, sid):
        if sid:
            return jsonify(**file_update_file(sid))
        ret = {
            'code': config.CODE_ERROR
        }
        return jsonify(**ret)


def category_list_all():
    ret = {
        'code': config.CODE_OK
    }
    items = Category.query.all()
    data = utils.jsonify_items(items)
    ret['items'] = data['items']
    ret['code'] = data['code']
    return ret


def category_list_by(args):
    ret = {
        'code': config.CODE_OK
    }
    data = utils.jsonify_items_by(Category, args)
    ret['items'] = data['items']
    ret['code'] = data['code']
    return ret


def category_retrieve_by(args):
    ret = {
        'code': config.CODE_OK
    }
    data = utils.jsonify_item_by(Category, args)
    ret['item'] = data['item']
    ret['code'] = data['code']
    return ret


class CategoryView(MethodView):

    methods = ['GET']

    def get(self):
        if not request.args:
            return jsonify(**category_list_all())
        return jsonify(**category_retrieve_by(request.args))


files_bp.add_url_rule('',
                      view_func=FileView.as_view(name='files_view'),
                      endpoint='files_view', strict_slashes=True)
files_bp.add_url_rule('/<string:sid>',
                      view_func=FileView.as_view(name='files_view'),
                      endpoint='files_view_sid', strict_slashes=True)

files_bp.add_url_rule('/categories',
                      view_func=CategoryView.as_view(name='categories_view'),
                      endpoint='categories_view', strict_slashes=True)
