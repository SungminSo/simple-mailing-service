from flask import request, Blueprint
from multiprocessing import Process

from . import json_response, v2_mail_host_list
from ..models.users import User, USERS_PER_PAGE
from ..utils.validate import validate_email
from ..config import Config

import requests

mail_api = Blueprint('mail', __name__)


def send_mail(subject: str, content: str, users: list, fail_to_send: list):
    for user in users:
        email_host = user.email.split("@")[1]
        if email_host in v2_mail_host_list:
            headers = {
                'Authorization': Config.HERRENCORP_MAIL_AUTH,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            url = Config.HERRENCORP_BASE_URL + Config.HERRENCORP_SEND_MAIL_URL_V2
        else:
            headers = {
                'Authorization': Config.HERRENCORP_MAIL_AUTH,
                'Content-Type': 'application/json',
            }
            url = Config.HERRENCORP_BASE_URL + Config.HERRENCORP_SEND_MAIL_URL

        data = {'mailto': user.email, 'subject': subject, 'content': content}

        res = requests.post(url, data=data, headers=headers)
        if res.status_code != 201:
            fail_to_send.append(user.email)


@mail_api.route('/mails', methods=['POST'])
def send_mail_to_all_users():
    try:
        req_data = request.get_json()
        subject = req_data['subject']
        content = req_data['content']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    try:
        if len(subject) == 0 or len(content) == 0:
            return json_response({'errorMsg': 'please check subject and content'}, 422)
    except TypeError:
        return json_response({'errorMsg': 'please check subject and content data type'}, 400)

    user_num = User.get_users_count()
    if user_num % USERS_PER_PAGE != 0:
        user_page = (user_num // USERS_PER_PAGE) + 1
    else:
        user_page = user_num // USERS_PER_PAGE

    fail_to_send = []
    procs = []
    for page in range(1, user_page + 1):
        users = User.get_all_users(page=page)
        proc = Process(target=send_mail, args=(subject, content, users.items, fail_to_send))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    if len(fail_to_send) != 0:
        return json_response({'errorMsg': f"fail to send email", 'fail_list': fail_to_send}, 500)
    return json_response({'status': 'success'}, 201)


@mail_api.route('/mails/<string:email>', methods=['GET'])
def get_user_mails(email: str):
    try:
        if not validate_email(email):
            return json_response({'errorMsg': 'wrong format of email'}, 422)
    except TypeError:
        return json_response({'errorMsg': 'please check email data type'}, 400)

    headers = {
        'Authorization': Config.HERRENCORP_MAIL_AUTH,
    }
    url = Config.HERRENCORP_BASE_URL + Config.HERRENCORP_GET_MAIL_URL + email
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return json_response({'errorMsg': res.json()}, res.status_code)

    return json_response({'mails': res.json()}, 200)
