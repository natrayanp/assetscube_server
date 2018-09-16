from . import bp_accallbk
from flask import redirect, request,make_response, jsonify
#from flask_cors import CORS, cross_origin
from assetscube.common import dbfunc as db
from assetscube.common import error_logics as errhand
from assetscube.common import jwtfuncs as jwtf
from assetscube.common import settings
from datetime import datetime
import pkgutil
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth



@bp_accallbk.route("/callback",methods=["GET","POST","OPTIONS"])
def callback():
    if request.method=="OPTIONS":
            print("inside callback options")
            response = "inside callback options"
            return make_response(jsonify(response), 200)

    elif request.method=="GET":
        print("inside callback get")
        params = request.args
        print(params)
        res_to_send = callback_handler(params)
        return redirect(res_to_send, 302)
        '''
        if res_to_send == 'success':
            resps = make_response(jsonify(resp), 200)
            #resps = make_response(jsonify(response), 200 if res_to_send == 'success' else 400)
        else:
            resps = make_response(jsonify(resp), 400)
        
        return resps
        '''

    elif request.method=="POST":
        print("inside callback post")
        res_to_send, response = callback_handler(callback_data)

        if res_to_send == 'success':
            resps = make_response(jsonify(response), 200)
            #resps = make_response(jsonify(response), 200 if res_to_send == 'success' else 400)
        else:
            resps = make_response(jsonify(response), 400)
        
        return resps    

def callback_handler(callback_data):
    print(callback_data["type"])
    if callback_data["type"] == "signup":
        url = clbk_singup_handler(callback_data)
    elif callback_data["type"] == "code":
        clbk_auth_handler(callback_data)
    return url

def clbk_singup_handler(callback_data):
    if callback_data["regdata"] == '401':
        # show error page
        return "http://localhost:4201/noti?type=signup&regdata=401&msg="+callback_data["msg"]
    else:
        # Do user registration here
        # Response data from nawalcube
        #ImmutableMultiDict([('type', 'signup'), ('regdata', '{uid:BgZEeC2nyzNeOZmHeTdASW4QsrB3,email:k.ananthi@gmail.com}'), ('msg', '')])@
        regsd = callback_data["regdata"]
        email = regsd["email"]
        # firebase auth setup
        try:
            print('inside try')
            default_app = firebase_admin.get_app('acfbapp')
            print('about inside try')
        except ValueError:
            print('inside value error')
            #cred = credentials.Certificate(os.path.dirname(__file__)+'/serviceAccountKey.json')
            cred = credentials.Certificate(settings.FBSERVICEAC)
            default_app = firebase_admin.initialize_app(credential=cred,name='acfbapp')
        else:
            pass

        print('app ready')        
        user = auth.create_user(email=email,app=default_app)
        print('Successfully fetched user data: {0}'.format(user.uid))

        print("inside callback singup success")
        

        
    
    return "ok"