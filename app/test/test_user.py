
def test_get_user_list_200(api):
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
