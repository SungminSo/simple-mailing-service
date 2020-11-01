from flask import request, Blueprint

from . import json_response
from ..models.users import User, USERS_PER_PAGE
from ..utils.validate import validate_email
from ..config import Config

import requests

mail_api = Blueprint('mail', __name__)


def send_mail(subject: str, content: str, users: list) -> list:
    fail_to_send = []
    for user in users:
        headers = {
            'Authorization': Config.HERRENCORP_MAIL_AUTH,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {'mailto': user.email, 'subject': subject, 'content': content}
        url = Config.HERRENCORP_BASE_URL + Config.HERRENCORP_SEND_MAIL_URL
        res = requests.post(url, data=data, headers=headers)
        if res.status_code != 201:
            fail_to_send.append(user.email)

    return fail_to_send


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
    # TODO: for문이 아니라 병렬처리로 처리해야함
    for page in range(1, user_page + 1):
        users = User.get_all_users(page=page)
        fail_to_send += send_mail(subject=subject, content=content, users=users.items)

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
