from .. import create_app

import pytest


@pytest.fixture
def api():
    app = create_app('test')
    assert app.config['TESTING'] == True
    assert app.config['POSTGRES_DB_NAME'] == 'mail_test'
    api = app.test_client()

    return api
