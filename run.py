from flask import Flask, request
import multiprocessing
import schedule
import time

from Service import Service
from SQLRepository import SQLRepositotry as sql

app = Flask(__name__)

@app.route('token', methods=['POST'])
def registerToken():
    # Service.registerToken()
    body = request.data
    token = body['token']['value']
    # user = body['user']['username']
    sql.registorUserToken(token)

@app.route('notification', methods=['POST'])
def addPushNotification(token, message, date):
    body = request.data
    token = body['token']['value']
    message = body['message']
    cycle = body['cycle']
    date = body['date']

    # TODO (?) 変数dateの内容をdatetimeオブジェクトに変換
    sql.schedulePushNotification(token, message, cycle, date)

if __name__ == '__main__':
    app.run()