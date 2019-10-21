from functools import wraps
from apps import utils
from apps.students import Student
from apps import config


def add_owner_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret['code'] != config.CODE_OK:
            return ret
        conditions = {
            'sid': ret['item']['sid']
        }
        ret['item']['owner'] = utils.jsonify_item_by(Student, conditions)['item']
        return ret
    return wrapper


def add_owners_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        for item in ret['items']:
            conditions = {
                'sid': item['sid']
            }
            item['owner'] = utils.jsonify_item_by(Student, conditions)['item']
        ret['studentNum'] = len(Student.query.all())
        return ret
    return wrapper
