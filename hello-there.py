import datetime
import os
import hmac
import hashlib

from flask import abort, Flask, jsonify, request

app = Flask(__name__)

def __generate_hmac_signature(timestamp, body):
    """
    hmacを作成

    :param timestamp Slackからのリクエスト.headerのタイムスタンプ情報
    :param body Slackからのリクエスト.body
    :return hmac
    """
    # Slack App - Basic Information - App Credentials に記載されている
    # Signing Secret
    secretkey = os.environ['SLACK_API_SIGNING_SECRET']
    secretkey_bytes = bytes(secretkey, 'UTF-8')

    message = "v0:{}:{}".format(timestamp, body)
    message_bytes = bytes(message, 'UTF-8')
    return hmac.new(secretkey_bytes, message_bytes, hashlib.sha256).hexdigest()

def is_request_valid(request):
    """
    有効なリクエストか判定

    :param request Slackからのリクエスト
    :return 有効なリクエストの場合True
    """
    if "X-Slack-Request-Timestamp" not in request.headers \
            or "X-Slack-Signature" not in request.headers:
        return False

    request_timestamp = int(request.headers["X-Slack-Request-Timestamp"])
    now_timestamp = int(datetime.datetime.now().timestamp())

    if abs(request_timestamp - now_timestamp) > (60 * 5):
        return False

    expected_hash = __generate_hmac_signature(
        request.headers["X-Slack-Request-Timestamp"],
        # キャッシュは有効、戻りはバイトではなくデコードされたユニコードにする
        request.get_data(True, True)
    )

    expected = "v0={}".format(expected_hash)
    actual = request.headers["X-Slack-Signature"]

    print(expected)
    print(actual)
    print(expected == actual)
    print(hmac.compare_digest(expected, actual))

    return hmac.compare_digest(expected, actual)

@app.route('/hello-there', methods=['POST'])
def hello_there():
    if not is_request_valid(request):
        abort(400)

    text = request.form['text']
    return jsonify(
        response_type='in_channel',
        text='<https://youtu.be/frszEJb0aOo|General Kenobi!>',
    )