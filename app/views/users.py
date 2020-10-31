from flask import request, Blueprint
from sqlalchemy.exc import IntegrityError

from . import json_response
from ..models import db
from ..models.users import User
from ..utils.validate import validate_email

import requests

# select 422 instead of 400 on validate failure
# notes: https://stackoverflow.com/questions/16133923/400-vs-422-response-to-post-of-data

user_api = Blueprint('user', __name__)


@user_api.route('/users/<int:page>', methods=['GET'])
def get_user_list(page: int):
    users = User.get_all_users(page=page)

    ret_users = []
    for user in users:
        ret_users.append({
            'uuid': user.uuid,
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at,
        })

    return json_response({'user': ret_users}, 200)


@user_api.route('/users/subscribe', methods=['POST'])
def subscribe_service():
    try:
        req_data = request.get_json()
        name = req_data['name']
        email = req_data['email']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    try:
        if len(name) == 0 or len(email) == 0:
            return json_response({'errorMsg': 'please check name and email'}, 422)
        if not validate_email(email):
            return json_response({'errorMsg': 'wrong format of email'}, 422)
    except TypeError:
        return json_response({'errorMsg': 'please check name and email data type'}, 400)

    user_already_exists = User.get_user_by_email(email)
    if user_already_exists:
        return json_response({'errorMsg': 'already subscribed'}, 409)

    user = User(
        name=name,
        email=email,
    )

    # # create a savepoint in case of race condition
    # db.session.begin_nested()
    # try:
    #     user_uuid = user.create()
    #     db.session.commit()
    #     return json_response({'uuid': user_uuid}, 201)
    # except IntegrityError:
    #     db.session.rollback()
    #     return json_response({'errorMsg': 'fail to subscribe'}, 409)
    user_uuid = user.create()
    db.session.commit()
    return json_response({'uuid': user_uuid}, 201)


@user_api.route('/users/unsubscribe/<string:uuid>/<string:email>', methods=['DELETE'])
def unsubscribe_service(uuid: str, email: str):
    if not validate_email(email):
        return json_response({'errorMsg': 'wrong format of email'}, 422)

    user = User.get_user_by_email(email)
    if not user:
        return json_response({'errorMsg': f"{email} does not subscribe to the subscribe"}, 404)

    if user.uuid != uuid:
        return json_response({'errorMsg': 'permission denied'}, 403)

    user.delete()
    db.session.commit()

    return json_response({}, 204)


@user_api.route('/mail', methods=['POST'])
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

    users = User.get_all_users(page=1)

    for user in users:
        headers = {
            'Authorization': 'herren-recruit-python',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {'mailto': user.email, 'subject': subject, 'content': content}
        res = requests.post('http://python.recruit.herrencorp.com/api/v1/mail', data=data, headers=headers)
        if res.status_code != 201:
            print(res.status_code)
            print(res.content)
            return json_response({'errorMsg': f"fail to send an email to {user.email}"}, 500)

    return json_response({'status': 'success'}, 201)
