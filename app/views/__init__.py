from flask import json, Response

v2_mail_host_list = [
    'gmail.com',
    'naver.com'
]


# select json.dumps instead of jsonify
# notes: https://velog.io/@matisse/flask-jsonify-%EC%99%80-json.dumps%EC%9D%98-%EC%B0%A8%EC%9D%B4
def json_response(res: dict, status_code: int) -> Response:
    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )
