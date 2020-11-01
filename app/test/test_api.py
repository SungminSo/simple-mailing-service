
def test_ping(api):
    resp = api.get("/")
    assert b'pong' in resp.data
