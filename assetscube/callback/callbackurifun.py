from . import bp_accallbk
from flask import redirect, request,make_response, jsonify
#from flask_cors import CORS, cross_origin
from assetscube.common import dbfunc as db
from assetscube.common import error_logics as errhand
from assetscube.common import jwtfuncs as jwtf
from assetscube.common import settings
from datetime import datetime



@bp_accallbk.route("/callback",methods=["GET","POST","OPTIONS"])
def callback():
    if request.method=="OPTIONS":
            print("inside callback options")
            response = "inside callback options"
            return make_response(jsonify(response), 200)

    elif request.method=="GET":
        print("inside callback get")
        params = request.args

        res_to_send, response = callback_handler(params)

        if res_to_send == 'success':
            resps = make_response(jsonify(response), 200)
            #resps = make_response(jsonify(response), 200 if res_to_send == 'success' else 400)
        else:
            resps = make_response(jsonify(response), 400)
        
        return resps

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
    if callback_data["type"] == "signup":
        return clbk_singup_handler(callback_data)
    elif callback_data["type"] == "code":
        clbk_auth_handler(callback_data)
    return "success" "ok"

def clbk_singup_handler(callback_data):
    if callback_data["regdata"] == '401':
        # show error page
        pass
    else:
        # Do user registration here
        pass
    
    return "ok"