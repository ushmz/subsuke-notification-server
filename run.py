from flask import Flask, request
from Service import Service
from SQLRepository import SQLRepositotry as sql

app = Flask(__name__)

@app.route('token', methods=['POST'])
def registerToken():
    Service.registerToken()
    body = request.data
    token = body['token']['value']
    # user = body['user']['username']
    sql.registorUserToken(token)

if __name__ == '__main__':
    app.run()