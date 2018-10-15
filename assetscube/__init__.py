from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app,supports_credentials=True)

#app.config.from_object('settings')

from assetscube.auth import bp_acauth, aclogin
from assetscube.callback import bp_accallbk, callbackurifun

app.register_blueprint(bp_acauth)
app.register_blueprint(bp_accallbk)

'''
@app.after_request
def remove_header(response):
    print("insdie")
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Origin, Content-Type, X-Auth-Token"

    return response
'''