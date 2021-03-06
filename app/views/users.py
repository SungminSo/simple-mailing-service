from flask import request, Blueprint

from . import json_response
from ..models import db
from ..models.users import User
from ..utils.validate import validate_email, validate_uuid

# select 422 instead of 400 on validate failure
# notes: https://stackoverflow.com/questions/16133923/400-vs-422-response-to-post-of-data

user_api = Blueprint('user', __name__)


@user_api.route('/users/<int:page>', methods=['GET'])
def get_user_list(page: int):
    users = User.get_all_users(page=page)
    if not users:
        return json_response({'errorMsg': 'no users in this page'}, 404)

    ret_users = []
    for user in users.items:
        ret_users.append({
            'uuid': user.uuid,
            'name': user.name,
            'email': user.email,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
        })

    return json_response({'total': users.total, 'users': ret_users}, 200)


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

    # TODO: race condition handling
    user_uuid = user.create()
    db.session.commit()
    return json_response({'uuid': user_uuid}, 201)


@user_api.route('/users/subscribe', methods=['PATCH'])
def change_subscribe_service_info():
    try:
        req_data = request.get_json()
        uuid = req_data['uuid']
        new_name = req_data['new_name']
        new_email = req_data['new_email']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    try:
        if len(uuid) == 0:
            return json_response({'errorMsg': 'please check uuid'}, 422)
        if not validate_uuid(uuid):
            return json_response({'errorMsg': 'wrong format of uuid'}, 422)

        if len(new_name) == 0 and len(new_email) == 0:
            return json_response({'errorMsg': 'please check new_name and new_email'}, 422)
        if not validate_email(new_email):
            return json_response({'errorMsg': 'wrong format of email'}, 422)
    except TypeError:
        return json_response({'errorMsg': 'please check uuid, new_name and new_email data type'}, 400)

    user = User.get_user_by_uuid(uuid)
    if not user:
        return json_response({'errorMsg': 'cannot found subscribe info'}, 404)

    user.update(new_name, new_email)
    db.session.commit()
    return json_response({'uuid': user.uuid}, 200)


@user_api.route('/users/subscribe/<string:uuid>/<string:email>', methods=['DELETE'])
def unsubscribe_service(uuid: str, email: str):
    try:
        if not validate_uuid(uuid):
            return json_response({'errorMsg': 'wrong format of uuid'}, 422)
        if not validate_email(email):
            return json_response({'errorMsg': 'wrong format of email'}, 422)
    except TypeError:
        return json_response({'errorMsg': 'please check uuid, email data type'}, 400)

    user = User.get_user_by_email(email)
    if not user:
        return json_response({'errorMsg': f"{email} does not subscribe to the subscribe"}, 404)

    if user.uuid != uuid:
        return json_response({'errorMsg': 'permission denied'}, 403)

    # TODO: race condition handling
    user.delete()
    db.session.commit()

    return json_response({}, 204)
