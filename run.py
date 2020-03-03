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
    body = request.get_json()
    token = body['token']['value']
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
    token = body['token']['value']
    message = body['notification']['message']
    cycle = body['notification']['cycle']
    date = body['notification']['date']

    sql.schedulePushNotification(rowid, token, message, cycle, date)

    resp = {
        'state': 'coding...'
    }
    return jsonify(resp)

@app.route('/notification/<int:rowid>', methods=['DELETE'])
def cancelScheduling(rowid):
    sql.cancelScheduling(rowid)
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

if __name__ == '__main__':
    app.run()

