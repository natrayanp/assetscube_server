from . import bp_accallbk
from flask import redirect, request,make_response, jsonify
#from flask_cors import CORS, cross_origin
from assetscube.common import dbfunc as db
from assetscube.common import error_logics as errhand
from assetscube.common import jwtfuncs as jwtf
from assetscube.common import settings as settings
from datetime import datetime
import pkgutil
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests

@bp_accallbk.route("/callback",methods=["GET","POST","OPTIONS"])
def callback():
    if request.method=="OPTIONS":
            print("inside callback options")
            response = "inside callback options"
            #print(request.headers)
            response1 = make_response(jsonify(response))
            #response1.headers['Origin'] = "http://localhost:5000"
            #response1.headers['Access-Control-Allow-Origin'] = "*"
            #response1.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
            #response1.headers['Access-Control-Allow-Headers'] = "Origin, entityid, Content-Type, X-Auth-Token, countryid"
            
            #print(response1.headers)
            
            return response1
            #return make_response(jsonify(response), 200)

    elif request.method=="GET":
        print("inside callback get")
        params = request.args
        print(params)
        callbk_proc_data = callback_handler(params)
        print(callbk_proc_data)
        print(type(callbk_proc_data))
        '''
                callbk_proc_data ={
                "typ": "signup",
                "regdata": "401",
                "msg": email + " registered failed.  Please retry.  If problem persists, please conatact support"
            }   
        '''
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
        print("inside callback POST")
        payload = request.get_json()
        print("payload 11111111")
        print(payload)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        entityid = request.headers.get("entityid", None)
        countryid = request.headers.get("countryid", None)
        payload["entityid"] = entityid
        payload["countryid"] = countryid 
        res_status, res_to_send = callback_handler(payload)

        if res_status == 'success':
            resps = make_response(jsonify(res_to_send), 200)
            #resps = make_response(jsonify(response), 200 if res_to_send == 'success' else 400)
        else:
            resps = make_response(jsonify(res_to_send), 400)
        
        return resps    

def callback_handler(callback_data):
    print("inside callback_handler")
    print(callback_data)
    print(callback_data["callbkfrm"])
    if callback_data["callbkfrm"] == "nawalcube":
        print("Inside nawalcube")
        return ncallbk_handler(callback_data)
    elif callback_data["callbkfrm"] == "upstox":
        #callbk_proc_data, status = clbk_auth_handler(callback_data)
        print("upstox")
    return  None, None

def ncallbk_handler(callback_data):
    if callback_data["type"] == "signup":
        return ncclbk_singup_handler(callback_data)


def ncclbk_singup_handler(callback_data):
    print("inside ncclbk_singup_handler function")
    s = 0
    f = None
    t = None #message to front end
    rec_status ="fail"
    print("nc signup handler")
    if callback_data["regdata"] == '401':
        # show error page
        print("signup handler error")
        callbk_proc_data ={
                "typ": "signup",
                "regdata": "401",
                "msg": "Registered failed.  Please retry.  If problem persists, please conatact support"
            }        
        return "fail", callbk_proc_data
    else:
        # Please register user and confirm
        
        #Get data from nawalcube
        headers = {"entityid":callback_data["entityid"], "countryid": callback_data["countryid"]}
        req_payload = {"userauthtkn": callback_data["regdata"], "appid": settings.NCAPPID[settings.LIVE],"appkey":settings.NCAPPKEY[settings.LIVE]}
        print("###########################")
        print(req_payload)
        print("###########################")
        r = requests.post(settings.NCSIGNUPDATAFETCHURL[settings.LIVE], headers=headers, data=json.dumps(req_payload))
        nc_usr_data = json.loads(r.content)
        print(json.loads(r.content))


        if nc_usr_data["status"] == "success":
            nc_email = nc_usr_data["emailid"]
            nc_userauthtkn = nc_usr_data["userauthtkn"]
            nc_usrid = nc_usr_data["userid"]

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
                user = auth.create_user(email=nc_email,app=default_app)
            except auth.AuthError as e:
                print(auth.ErrorInfo)
                #e.code == "USER_CREATE_ERROR":
                print(e.code)
                print(e.detail)
                print("Auth error while creating user")
                s = 100
            except ValueError as e:
                print("value error while creating user")
                s = 100
            else:
                print(user.uid)
                print(format(user))

            print("inside callback singup success")
        if s > 0:
            rec_status ="fail"
            callbk_proc_data ={
                "typ": "signup",
                "regdata": "401",
                "msg": nc_email + " registered failed.  Please retry.  If problem persists, please conatact support"
            }
        else:
            rec_status ="success"
            callbk_proc_data = {
                "typ": "signup",
                "regdata": "200",
                "msg": nc_email + " registered successfully.  Please reset password before first login"
            }
        
        return  rec_status, callbk_proc_data