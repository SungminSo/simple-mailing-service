import json


def test_send_mail_to_all_users(api):
    data = {'subject': 'test_subject', 'content': 'test_content'}
    res = api.post('/api/v1/mails', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 201


def test_send_mail_to_all_users_400(api):
    res = api.post('/api/v1/mails', data=json.dumps({}), content_type='application/json')
    assert res.status_code == 400
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check your request data'

    data = {'subject': 1, 'content': 1}
    res = api.post('/api/v1/mails', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check subject and content data type'


def test_send_mail_to_all_users_422(api):
    data = {'subject': '', 'content': ''}
    res = api.post('/api/v1/mails', data=json.dumps(data), content_type='application/json')
    assert res.status_code == 422
    error_msg = res.json['errorMsg']
    assert error_msg == 'please check subject and content'


def test_get_user_mails(api):
    email = 'test@gmail.com'
    res = api.get(f'/api/v1/mails/{email}')
    assert res.status_code == 200

    mails = res.json['mails']
    assert type(mails) == list


def test_get_user_mails_422(api):
    email = 'test'
    res = api.get(f'/api/v1/mails/{email}')
    assert res.status_code == 422

    error_msg = res.json['errorMsg']
    assert error_msg == 'wrong format of email'
