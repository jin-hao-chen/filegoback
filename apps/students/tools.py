import json
import requests
import base64
import uuid


def get_token():
    url = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = "client_credentials"
    api_key = "0b7ybOzfloChuuzUlGxyiY1i"
    secret_key = "CtsmtzPp94kskXSMPyb5RdcpbrAL7zyH"
    data = {'grant_type': 'client_credentials', 'client_id': api_key, 'client_secret': secret_key}
    r = requests.post(url, data=data)
    token = json.loads(r.text).get("access_token")
    return token


def recognize(token, image_base64):
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=' + token
    data = {
        'image': image_base64,
        'image_type': 'BASE64',
        'group_id_list': 'Students'
    }
    data_length = len(json.dumps(data).encode('utf-8'))
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': str(data_length)
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    text_json = json.loads(r.text)
    if text_json['error_code'] != 0:
        return None
    ret = {
        'sid': text_json['result']['user_list'][0]['user_id'],
        'score': text_json['result']['user_list'][0]['score']
    }
    return ret
