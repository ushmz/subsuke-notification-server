from flask import Flask, jsonify, request
import multiprocessing
import schedule
import time

from NotificationScheduler import NotificationScheduler as scheduler
from Service import Service
from SQLRepository import SQLRepository

app = Flask(__name__)

sql = SQLRepository()

s = scheduler()
s.execute()


@app.route('/token', methods=['POST'])
def registerToken():
    body = request.get_json()
    token = body['token']['value']
    # user = body['user']['username']
    sql.registorUserToken(token=token)
    resp = {
        'state': 'coding...'
    }
    return jsonify(resp)

@app.route('/notification', methods=['POST'])
def addPushNotification():
    body = request.get_json()
    token = body['token']['value']
    message = body['notification']['message']
    cycle = body['notification']['cycle']
    date = body['notification']['date']

    # TODO (?) 変数dateの内容をdatetimeオブジェクトに変換
    sql.schedulePushNotification(token, message, cycle, date)

    resp = {
        'state': 'coding...'
    }
    return jsonify(resp)


if __name__ == '__main__':
    app.run()
