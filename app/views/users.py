from flask import request, Blueprint
from sqlalchemy.exc import IntegrityError

from . import json_response
from ..models import db
from ..models.users import User
from ..utils.validate import validate_email

user_api = Blueprint('user', __name__)


@user_api.route('/subscribe', methods=['POST'])
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
        # select 422 instead of 400 on validate failure
        # notes: https://stackoverflow.com/questions/16133923/400-vs-422-response-to-post-of-data
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

    # create a savepoint in case of race condition
    db.session.begin_nested()
    try:
        user_uuid = user.create()
        db.session.commit()
        return json_response({'uuid': user_uuid}, 201)
    except IntegrityError:
        db.session.rollback()
        return json_response({'errorMsg': 'fail to subscribe'}, 409)
