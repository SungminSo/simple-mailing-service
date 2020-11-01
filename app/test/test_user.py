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

    uuid_str = res.json['uuid']
    assert type(uuid.UUID(uuid_str)) == uuid.UUID


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
    uuid_str = res.json['uuid']
    assert type(uuid.UUID(uuid_str)) == uuid.UUID

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
