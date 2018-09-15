from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app,supports_credentials=True)

#app.config.from_object('settings')

from assetscube.auth import bp_acauth, aclogin

app.register_blueprint(bp_acauth)