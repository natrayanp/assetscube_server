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
import json



@bp_accallbk.route("/callback",methods=["GET","POST","OPTIONS"])
def callback():
    if request.method=="OPTIONS":
            print("inside callback options")
            response = "inside callback options"
            print(request.headers)
            response1 = make_response(jsonify(response))
            response1.headers['Origin'] = "http://localhost:5000"
            response1.headers['Access-Control-Allow-Origin'] = "*"
            response1.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
            response1.headers['Access-Control-Allow-Headers'] = "Origin, entityid, Content-Type, X-Auth-Token, countryid"
            
            print(response1.headers)
            
            return response1
            #return make_response(jsonify(response), 200)

    elif request.method=="GET":
        print("inside callback get")
        params = request.args
        print(params)
        callbk_proc_data = callback_handler(params)
        typ = callbk_proc_data["typ"]
        regdata = callbk_proc_data["regdata"]
        msg = callbk_proc_data["msg"]
        print(typ, regdata, msg)
        print(settings.MYNOTIPG[settings.LIVE])
 
        response1 = make_response(redirect(settings.MYNOTIPG[settings.LIVE]+"?type="+typ+"&regdata="+regdata+"&msg="+msg, code=302))
        response1.headers['Origin'] = "http://localhost:5000"
        del response1.headers['entityid']
        del response1.headers['coutnrycode']
        response1.headers['Access-Control-Allow-Origin'] = "*"
        response1.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
        response1.headers['Access-Control-Allow-Headers'] = "Origin, entityid, Content-Type, X-Auth-Token, countryid"
        print(response1.headers)
        return response1
        #return redirect(settings.MYNOTIPG[settings.LIVE]+"?type="+typ+"&regdata="+regdata+"&msg="+msg, code=302)

        


        '''
        #
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
        return clbk_singup_handler(callback_data)
    elif callback_data["type"] == "code":
        #callbk_proc_data, status = clbk_auth_handler(callback_data)
        pass
    return  None, None

def clbk_singup_handler(callback_data):
    print("signup handler")
    if callback_data["regdata"] == '401':
        # show error page
        print("signup handler error")

        return "http://localhost:4201/noti?type=signup&regdata=401&msg="+callback_data["msg"]
    else:
        # Do user registration here
        # Response data from nawalcube
        #ImmutableMultiDict([('type', 'signup'), ('regdata', '{uid:BgZEeC2nyzNeOZmHeTdASW4QsrB3,email:k.ananthi@gmail.com}'), ('msg', '')])@
        print("signup handler success :)")
        regsd = json.loads(callback_data["regdata"])        
        print(regsd)
        print(type(regsd))
        email = regsd["email"]
        print(email)
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
        try: 
            user = auth.create_user(email=email,app=default_app)
        except auth.AuthError as e:
            #e.code == "USER_CREATE_ERROR":
            print("inside callback singup success")
            callbk_proc_data ={
                "typ": "signup",
                "regdata": "401",
                "msg": email + " registered failed.  Please retry.  If problem persists, please conatact support"
            }
        else:
            callbk_proc_data = {
                "typ": "signup",
                "regdata": "200",
                "msg": email + " registered successfully.  Please reset password before first login"
            }
        
        return  callbk_proc_data
        ''''
            print('inside Auth error')
            print(e)
            print(type(e))
            print("-------")
            print(e.code)
            print("-------222")
            print(e.detail)
            print(e.args)
            print(e.message)

            print('Successfully fetched user data: {0}'.format(user.uid))

        
        

        
    
            return "ok"
        '''