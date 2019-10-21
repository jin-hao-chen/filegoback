from flask import Blueprint
from flask.views import MethodView
from flask import (request, jsonify)
from apps.students.models import Student
from apps.students import tools
from apps import utils
from apps import config


students_bp = Blueprint('students', __name__)


def student_retrieve(sid):
    ret = {
        'code': config.CODE_OK
    }
    conditions = {
        'sid': sid
    }
    data = utils.jsonify_item_by(Student, conditions)
    ret['item'] = data['item']
    ret['code'] = data['code']
    return ret


def student_list_all():
    ret = {
        'code': config.CODE_OK
    }
    items = Student.query.all()
    data = utils.jsonify_items(items)
    ret['items'] = data['items']
    ret['code'] = data['code']
    return ret


def student_list_by(args):
    ret = {
        'code': config.CODE_OK
    }
    data = utils.jsonify_items_by(Student, args)
    ret['items'] = data['items']
    ret['code'] = data['code']
    return ret


def student_admin_login(image_base64):
    ret = {
        'code': config.CODE_OK
    }
    token = tools.get_token()
    result = tools.recognize(token, image_base64)
    if result is None:
        ret['code'] = config.CODE_ERROR02
        return ret
    sid = result['sid']
    if result['score'] < 95:
        ret['code'] = config.CODE_ERROR
        return ret
    data = utils.jsonify_item_by(Student, {
        'sid': sid
    })
    ret['item'] = data['item']
    ret['code'] = data['code']
    return ret


class StudentView(MethodView):

    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def get(self, sid=None):
        # retrieve
        if sid:
            return jsonify(**student_retrieve(sid))
        # list
        if not request.args:
            return jsonify(**student_list_all())
        return jsonify(**student_list_by(request.args))

    def post(self):
        img_base64 = request.form.get('img')
        if img_base64:
            return jsonify(**student_admin_login(img_base64))


students_bp.add_url_rule('', view_func=StudentView.as_view(name='student_view'),
                         endpoint='student_view',
                         strict_slashes=True)

students_bp.add_url_rule('/<string:sid>',
                         view_func=StudentView.as_view(name='student_view'),
                         endpoint='student_view_sid',
                         strict_slashes=True)
