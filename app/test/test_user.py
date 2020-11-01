import uuid
import json


def test_get_user_list(api):
    res = api.get(f"/api/v1/users/{1}")
    assert res.status_code == 200

    total = res.json['total']
    assert type(total) == int

    users = res.json['users']
    assert type(users) == list


def test_get_user_list_404(api):
    res = api.get(f"/api/v1/users/{10000}")
    assert res.status_code == 404

    error_msg = res.json['errorMsg']
    assert error_msg == 'no users in this page'


def test_subscribe_service(api):
    data = {'name': 'test', 'email': 'test@gmail.com'}
    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 201

    user_uuid = res.json['uuid']
    assert type(uuid.UUID(user_uuid)) == uuid.UUID


def test_subscribe_service_400(api):
    res = api.post('/api/v1/users/subscribe', data=json.dumps({}), content_type='application/json')
    assert res.status_code == 400
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check your request data'

    data = {'name': 1, 'email': 1}
    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check name and email data type'


def test_subscribe_service_409(api):
    data = {'name': 'test1', 'email': 'test1@gmail.com'}
    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 201
    user_uuid = res.json['uuid']
    assert type(uuid.UUID(user_uuid)) == uuid.UUID

    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 409
    error_msg = res.json['errorMsg']
    assert error_msg == 'already subscribed'


def test_subscribe_service_422(api):
    data = {'name': '', 'email': ''}
    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check name and email'

    data = {'name': 'test2', 'email': 'test2'}
    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'wrong format of email'


def test_change_subscribe_service_info(api):
    data = {'name': 'test_info', 'email': 'test_info@gmail.com'}
    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 201
    user_uuid = res.json['uuid']
    assert type(uuid.UUID(user_uuid)) == uuid.UUID

    data = {'uuid': user_uuid, 'new_name': 'new_test_info', 'new_email': 'new_test_info@gmail.com'}
    res = api.patch('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 200
    assert res.json['uuid'] == user_uuid


def test_change_subscribe_service_info_400(api):
    res = api.patch('/api/v1/users/subscribe', data=json.dumps({}), content_type='application/json')
    assert res.status_code == 400
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check your request data'

    data = {'uuid': str(uuid.uuid4()), 'new_name': 1, 'new_email': 1}
    res = api.patch('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check uuid, new_name and new_email data type'

    data = {'uuid': 11, 'new_name': 'new_test_info', 'new_email': 'new_test_info@gmail.com'}
    res = api.patch('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check uuid, new_name and new_email data type'


def test_change_subscribe_service_info_404(api):
    data = {'uuid': str(uuid.uuid4()), 'new_name': 'new_test_info1', 'new_email': 'new_test_info1@gmail.com'}
    res = api.patch('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 404
    error_msg = res.json['errorMsg']
    assert error_msg == 'cannot found subscribe info'


def test_change_subscribe_service_info_422(api):
    data = {'uuid': '', 'new_name': 'new_test_info1', 'new_email': 'new_test_info1@gmail.com'}
    res = api.patch('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check uuid'

    data = {'uuid': 'uuid', 'new_name': 'new_test_info1', 'new_email': 'new_test_info1@gmail.com'}
    res = api.patch('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'wrong format of uuid'

    data = {'uuid': str(uuid.uuid4()), 'new_name': '', 'new_email': ''}
    res = api.patch('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check new_name and new_email'

    data = {'uuid': str(uuid.uuid4()), 'new_name': 'new_test_info1', 'new_email': 'new_test_info1'}
    res = api.patch('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'wrong format of email'


def test_unsubscribe_service(api):
    email = 'test11@gmail.com'
    data = {'name': 'test11', 'email': email}
    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 201
    user_uuid = res.json['uuid']
    assert type(uuid.UUID(user_uuid)) == uuid.UUID

    res = api.delete(f'/api/v1/users/subscribe/{user_uuid}/{email}')
    assert res.status_code == 204


def test_unsubscribe_service_403(api):
    email = 'test12@gmail.com'
    data = {'name': 'test12', 'email': email}
    res = api.post('/api/v1/users/subscribe', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 201
    user_uuid = res.json['uuid']
    assert type(uuid.UUID(user_uuid)) == uuid.UUID

    res = api.delete(f'/api/v1/users/subscribe/{str(uuid.uuid4())}/{email}')
    assert res.status_code == 403
    error_msg = res.json['errorMsg']
    assert error_msg == 'permission denied'


def test_unsubscribe_service_404(api):
    email = 'test13@gmail.com'
    res = api.delete(f'/api/v1/users/subscribe/{str(uuid.uuid4())}/{email}')
    assert res.status_code == 404

    error_msg = res.json['errorMsg']
    assert error_msg == f'{email} does not subscribe to the subscribe'


def test_unsubscribe_service_422(api):
    res = api.delete(f'/api/v1/users/subscribe/{"uuid"}/{"test13@gmail.com"}')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'wrong format of uuid'

    res = api.delete(f'/api/v1/users/subscribe/{str(uuid.uuid4())}/{"email"}')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'wrong format of email'
