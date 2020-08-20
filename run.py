from flask import Flask, jsonify, request
import multiprocessing
import schedule
import time

from NotificationScheduler import NotificationScheduler as scheduler
from Service import Service
from SQLRepository import SQLRepository

app = Flask(__name__)

sql = SQLRepository()


@app.route('/')
def home():
    return 'run'

@app.route('/token', methods=['POST'])
def registerToken():
    '''
    {domain}/tokenにPOSTされた場合に，bodyからトークンを取得しデータベースに登録する

    Action:
        http(POST)
    Returns:
        resp(str) : アプリ側に返すレスポンス
    '''
    body = request.get_json()
    token = body['pushtoken']
    # user = body['user']['username']
    sql.registorUserToken(token=token)
    resp = {
        'state': 'coding...',
        'token': token
    }
    return jsonify(resp)

@app.route('/notification', methods=['POST'])
def addPushNotification():
    body = request.get_json()
    rowid = body['notification']['rowid']
    token = body['pushtoken']
    message = body['notification']['message']
    cycle = body['notification']['cycle']
    date = body['notification']['date']

    sql.schedulePushNotification(rowid, token, message, cycle, date)

    resp = {
        'state': 'coding...'
    }
    return jsonify(resp)

@app.route('/notification/<string:params>', methods=['DELETE'])
def cancelScheduling(params):
    rowid, token = params.split(':')
    sql.cancelScheduling(rowid, token)
    resp = {
        'state': 'coding...'
    }
    return jsonify(resp)

@app.route('/notification/upd', methods=['POST'])
def updateScheduling():
    body = request.get_json()
    token = body['pushtoken']
    rowid = body['notification']['rowid']
    update = body['update']
    sql.updateNotification(token, rowid, update)
    resp = {
        'state': 'coding...'
    }
    return jsonify(resp)


@app.route('/notification/upd', methods=['PATCH'])
def updateScheduling_UNUSE():
    body = request.get_json()
    token = body['pushtoken']
    rowid = body['notification']['rowid']
    update = body['update']
    sql.updateNotification(token, rowid, update)
    resp = {
        'state': 'coding...'
    }
    return jsonify(resp)

@app.route('/send', methods=['POST'])
def sendNotification():
    s = scheduler()
    s.execute()
    resp = {
        'state': 'coding...'
    }
    return jsonify(resp)

@app.route('/test/send', methods=['POST'])
def sendTestNotification():
    body = request.get_json()
    token = body.token
    message = body.message
    service = Service()
    # service.sendPushNotfication('ExponentPushToken[3aGDhnPfT80I2I121sKa7L]', message, body)

if __name__ == '__main__':
    app.run(debug=True)

