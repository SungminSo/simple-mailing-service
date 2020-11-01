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


