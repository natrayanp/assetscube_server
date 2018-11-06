from . import bp_acauth
from flask import redirect, request,make_response, jsonify
#from flask_cors import CORS, cross_origin
from assetscube.common import dbfunc as db
from assetscube.common import error_logics as errhand
from assetscube.common import jwtfuncs as jwtf
from assetscube.common import settings
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import os
import hashlib



@bp_acauth.route("/acsignup",methods=["GET","POST","OPTIONS"])
def signup():
    if request.method=="OPTIONS":
            print("inside signup options")
            response1 = make_response(jsonify("inside signup options"),200)
            '''
            response1.headers['Access-Control-Allow-Origin'] = "*"
            response1.headers['Access-Control-Allow-Methods'] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
            response1.headers['Access-Control-Allow-Headers'] = "Origin, entityid, Content-Type, X-Auth-Token"
            print(response1.headers)
            '''
            return response1

    elif request.method=="GET":
        res_to_send, response = signup_common()

        if res_to_send == 'success':
            resps = make_response(jsonify(response), 200)
            #resps = make_response(jsonify(response), 200 if res_to_send == 'success' else 400)
        else:
            resps = make_response(jsonify(response), 400)
        
        return resps


def signup_common():
    url = settings.NCREGURL[settings.LIVE]+'?type=signup&appid='+settings.NCAPPID[settings.LIVE]+'&home='+settings.MYHOMEPG[settings.LIVE]+'&redirecturi='+settings.MYREDIRURI[settings.LIVE]
    print(url)
    repons = {'url':url}
    return 'success', repons



@bp_acauth.route("/aclogin",methods=["GET","POST","OPTIONS"])
def aclogin():
    if request.method=="OPTIONS":
            print("inside aclogin options")
            response1 = make_response(jsonify("inside aclogin options"),200)
            return response1

    elif request.method=="POST":
        res_to_send, response = aclogin_common()

        if res_to_send == 'success':
            resps = make_response(jsonify(response), 200)
            #resps = make_response(jsonify(response), 200 if res_to_send == 'success' else 400)
        else:
            resps = make_response(jsonify(response), 400)
        
        return resps


def aclogin_common():
    url = settings.NCLOGINURL[settings.LIVE]+'?request=code&appid='+settings.NCAPPID[settings.LIVE]+'&redirecturi='+settings.MYREDIRURI[settings.LIVE]
    print(url)
    repons = {'url':url}
    return 'success', repons


'''


        print("inside signup POST")
        s = 0
        f = None
        t = None #message to front end
        payload = request.get_json()
        print(payload)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))








        
        print(s)
        if s <= 0:

            if payload.get("custtype", None) != None:
                usercusttype = payload['custtype']['value']
            else:
                usercusttype = None
                s, f, t= errhand.get_status(s, 100, f, "No user customer type from client", t, "yes")

            if payload.get("name", None) != None:
                sinupusername = payload['name']
            else:
                sinupusername = None
                s, f, t= errhand.get_status(s, 100, f, "No user name from client", t, "yes")

            if payload.get("adhaar", None) != None:
                sinupadhaar = payload['adhaar']
            else:
                sinupadhaar = None
                if usercusttype not in ['D','A','T']:                    
                    s, f, t= errhand.get_status(s, 100, f, "No adhaar from client", t, "yes")
                    
            if payload.get("pan", None) != None:
                sinuppan = payload['pan']
            else:
                sinuppan = None
                if usercusttype not in ['D','A','T']:                    
                    s, f, t= errhand.get_status(s, 100, f, "No pan from client", t, "yes")
            
            if payload.get("arn", None) != None:
                sinuparn = payload['arn']
            else:
                sinuparn = None
                if usercusttype not in ['I']:                    
                    s, f, t= errhand.get_status(s, 100, f, "No arn from client", t, "yes")

            if payload.get("mobile", None) != None:
                sinupmobile = payload['mobile']
            else:
                sinupmobile = None
                s, f, t= errhand.get_status(s, 100, f, "No mobile data from client", t, "yes")       

            usertype='W'
            userstatus = 'S'
            cur_time = datetime.now().strftime('%Y%m%d%H%M%S')
            print(sinupadhaar,sinuppan,sinuparn,sinupmobile)
        # firebase auth setup
        print(os.path.dirname(__file__)+'/serviceAccountKey.json')
        try:
            print('inside try')
            default_app=firebase_admin.get_app('natfbloginsingupapp')
            print('about inside try')
        except ValueError:
            print('inside value error')
            cred = credentials.Certificate(os.path.dirname(__file__)+'/serviceAccountKey.json')
            default_app = firebase_admin.initialize_app(credential=cred,name='natfbloginsingupapp')
        else:
            pass

        print('app ready')
        
        try:
            print('start decode')
            decoded_token = auth.verify_id_token(token,app=default_app)
            print('decoded')
        except ValueError:
            print('valuererror')
            s, f, t = errhand.get_status(s, 100, f, "Not a valid user properties", t, "yes")            
        except AuthError:
            print('AuthError')
            s, f, t = errhand.get_status(s, 100, f, "Not a valid user credentials", t, "yes")     
        else:
            print('inside', decoded_token)
            uid = decoded_token.get("user_id", None)
            exp = decoded_token.get("exp", None)
            iat = decoded_token.get("iat", None)
            email = decoded_token.get("email", None)
            # set entity id to the token
            entityid = request.headers.get("entityid", None)
            cntryid = request.headers.get("countryid", None)
            
            if entityid != None:
                try:
                    print('start set custom')
                    auth.set_custom_user_claims(uid, {"entityid": entityid, "countryid": cntryid, "custtype": usercusttype},app=default_app)
                    print('end set custom')
                except ValueError:
                    print('valuererror')
                    s, f, t = errhand.get_status(s, 100, f, "Not a valid user properties", t, "yes")
                except AuthError:
                    print('AuthError')
                    s, f, t = errhand.get_status(s, 100, f, "Not a valid user credentials", t, "yes")
            else:
                print('else after autherror')
                s, f, t = errhand.get_status(s, 100, f, "No entity id from client", t, "yes")

            print('apppa mudichachu')
            print(uid)
            print(decoded_token)
        

        if s <= 0:
            if email != None:
                sinupemail = email
            else:
                sinupemail = None
                s, f, t = errhand.get_status(s, 100, f, "No email data from client", t, "yes")

            if uid != None:
                userid = uid
            else:
                userid = None
                s, f, t = errhand.get_status(s, 100, f, "No user id from client" , t, "yes")
        
        
        if s <= 0:
            con, cur, s1, f1 = db.mydbopncon()
            s, f, t = errhand.get_status(s, s1, f, f1, t, "no")
            s1, f1 = 0, None
        

        if s <= 0:
            command = cur.mogrify("""
                                    SELECT json_agg(a) FROM (
                                    SELECT l.userid, l.username, l.usertype, l.usercusttype, l.entityid, 
                                    d.sinupusername, d.sinupadhaar, d.sinuppan, d.sinupmobile, d.sinupemail, d.sinuparn
                                    FROM ncusr.userlogin l
                                    LEFT JOIN ncusr.userdetails d ON l.userid = d.userid AND l.entityid = d.entityid
                                    WHERE l.userstatus != 'I'
                                    AND (
                                            l.userid = %s OR d.sinupadhaar = %s OR d.sinuppan = %s OR sinuparn = %s OR d.sinupmobile = %s OR d.sinupemail = %s
                                        )
                                    AND l.entityid = %s AND l.countryid = %s
                                    ) as a
                                """,(uid,sinupadhaar,sinuppan,sinuparn,sinupmobile,sinupemail,entityid,cntryid,) )
            print(command)
            cur, s1, f1 = db.mydbfunc(con,cur,command)
            s, f, t = errhand.get_status(s, s1, f, f1, t, "no")
            s1, f1 = 0, None
            print('----------------')
            print(s)
            print(f)
            print('----------------')
            if s > 0:
                s, f, t = errhand.get_status(s, 200, f, "User data fetch failed with DB error", t, "no")
        print(s,f)

        if s <= 0:
            db_json_rec = cur.fetchall()[0][0]
            print(db_json_rec)

            if db_json_rec:
                for rec in db_json_rec:
                    if rec['userid'] != '':
                        if rec['userid'] == userid:
                            s, f, t= errhand.get_status(s, 100, f, "Userid Already exists", t, "yes")

                    if rec['sinupadhaar'] != '':           
                        if rec['sinupadhaar'] == sinupadhaar:
                            s, f, t= errhand.get_status(s, 100, f, "Adhaar Already registered", t, "yes")

                    if rec['sinuppan'] != '':
                        if rec['sinuppan'] == sinuppan:
                            s, f, t= errhand.get_status(s, 100, f, "PAN Already registered", t, "yes")

                    if rec['sinuparn'] != '':
                        if rec['sinuparn'] == sinuppan:
                            s, f, t= errhand.get_status(s, 100, f, "ARN Already registered", t, "yes")

                    if rec['sinupmobile'] != '':
                        if rec['sinupmobile'] == sinupmobile:
                            s, f, t= errhand.get_status(s, 100, f, "Mobile Already registered", t, "yes")

                    if rec['sinupemail'] != '':
                        if rec['sinupemail'] == sinupemail:
                            s, f, t= errhand.get_status(s, 100, f, "Email Already registered", t, "yes")
            else:
                print("no records satifying the current user inputs")
        print(s,f)
        if s <= 0:
            s1, f1 = db.mydbbegin(con, cur)
            print(s1,f1)

            s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
            s1, f1 = 0, None

        if s <= 0:
            command = cur.mogrify("""
                        INSERT INTO ncusr.userlogin (userid, usertype, usercusttype, userstatus, userstatlstupdt, octime, lmtime, entityid, countryid) 
                        VALUES (%s,%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,%s,%s);
                        """,(userid, usertype, usercusttype, userstatus, entityid, cntryid,))
            print(command)
            cur, s1, f1 = db.mydbfunc(con,cur,command)
            s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
            s1, f1 = 0, None

            if s > 0:
                s, f, t= errhand.get_status(s, 200, f, "SIGNUP update failed", t, "no")
            print('Insert or update is successful')

        if s <= 0:
            command = cur.mogrify("""
                        INSERT INTO ncusr.userdetails (userid, sinupusername, sinupadhaar, sinuppan, sinuparn, sinupmobile, sinupemail, octime, lmtime, entityid, countryid) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,%s,%s);
                        """,(userid, sinupusername, sinupadhaar, sinuppan, sinuparn, sinupmobile, sinupemail, entityid, cntryid,))
            print(command)
            cur, s1, f1 = db.mydbfunc(con,cur,command)
            s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
            s1, f1 = 0, None

            if s > 0:
                s, f, t= errhand.get_status(s, 200, f, "SIGNUP update failed", t, "no")

            print('Insert or update is successful')
    
        if s <= 0:
            con.commit()
            #validate PAN adn store PAN number

            response = {
                'status': 'success',
                'error_msg' : ''
            }
            resps = make_response(jsonify(response), 200)
        else:
            response = {
                'status': 'fail',
                'error_msg' : errhand.error_msg_reporting(s, t)
            }
            resps = make_response(jsonify(response), 400)
        
        return resps
'''