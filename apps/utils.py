# -*- coding: utf-8 -*-

import re
import datetime
from sqlalchemy.orm.collections import InstrumentedList
from apps import db
from apps import config


def serialize(model):
    props = [prop for prop in dir(model) if not prop.startswith('_')]
    props.remove('metadata')
    props.remove('query_class')
    props.remove('query')

    obj = {}
    for name in props:
        prop = getattr(model, name)
        if isinstance(prop, db.Model) or isinstance(prop, InstrumentedList):
            continue
        if isinstance(prop, datetime.datetime):
            prop = getattr(prop, 'strftime')('%Y-%m-%d %H:%M:%S')
        obj[name] = prop
    return obj


def jsonify_items(items):
    data = []
    for item in items:
        data.append(serialize(item))
    ret = {
        'code': config.CODE_OK,
        'items': data
    }
    return ret


def jsonify_items_by(model, conditions):
    items = model.query.filter_by(**conditions).all()
    return jsonify_items(items)


def jsonify_item_by(model, conditions):
    items = model.query.filter_by(**conditions).all()
    ret = {
        'code': config.CODE_OK
    }
    if len(items) == 0:
        ret['code'] = config.CODE_ERROR
        ret['item'] = None
        return ret
    ret['item'] = serialize(items[0])
    return ret


def fetch_sid(filename):
    regex = re.compile('[0-9]{10}')
    sid = regex.findall(filename)
    if len(sid) == 0:
        return None
    return sid[0]


def get_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')