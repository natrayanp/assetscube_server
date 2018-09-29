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
    usrmsg = None
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
            nc_tknexpiry = nc_usr_data["tknexpiry"]
            nc_usrid = nc_usr_data["userid"]
            nc_usrname = nc_usr_data["username"]

            #initialise the Firebase app
            try:
                print('inside try')
                default_app = firebase_admin.get_app('acfbapp')
                print('about inside try')
            except ValueError:
                print('inside value error')
                #cred = credentials.Certificate(os.path.dirname(__file__)+'/serviceAccountKey.json')
                cred = credentials.Certificate(settings.FBSERVICEAC)
                default_app = firebase_admin.initialize_app(credential=cred,name='acfbapp')
                s, f, t= errhand.get_status(s, 0, f, "Firebase app initialised", t, "no")
            else:
                pass
            
            print('app initialisation completed')
            #TO check if the email already exists
            useridex = False
            if s <= 0:
                try: 
                    user = auth.get_user_by_email(nc_email,app=default_app)
                    print('Successfully fetched user data: {0}'.format(user.uid))
                except auth.AuthError as e:
                    print(str(e.args))
                    s, f, t= errhand.get_status(s, 0, f, ''.join(e.args), t, "no")   
                except Exception as inst:
                    print(inst.args)
                    print(inst)
                    s, f, t= errhand.get_status(s, 0, f, inst, t, "no")
                else:
                    if user.uid != None or user.uid != "":
                        useridex = True

                    print("user details fetch successful")
                    s, f, t= errhand.get_status(s, 0, f, " email already registered.", t, "yes")
                    usrmsg = "email already registered."
            print(useridex)
            #If email already exists skip fb user creation
            if s <= 0 and (not useridex):
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
                    s, f, t= errhand.get_status(s, 0, f, "Firebase app user details fetch failed", t, "no")
                    s, f, t= errhand.get_status(s, 100, f, "User registration failed.  Please cotact support [ac error]", t, "yes")
                else:
                    print(user.uid)
                    print(format(user))
                    s, f, t= errhand.get_status(s, 0, f, "registeration successful.", t, "no")
            print("inside callback singup success")

        else:
            s, f, t= errhand.get_status(s, 100, f, "User registration failed.  Please contact support [nc fetch].", t, "yes")

        if s >= 0:
            sav_usr = {
                "uid": user.uid,
                "nc_email" : nc_email,
                "nc_userauthtkn" : nc_userauthtkn,
                "nc_tknexpiry" : nc_tknexpiry,
                "nc_usrid" : nc_usrid,
                "nc_usrname" : nc_usrname,
                "nc_entity": "NAWALCUBE"
            }
            sav_status, sav_resp_rec = save_usr_details(sav_usr)
            if sav_status != "success":
                print(sav_resp_rec)
                s, f, t= errhand.get_status(s, 100, f, "User registration failed.  Please contact support [ac db update].", t, "yes")

            

        if s >= 0:
            rec_status ="fail"
            usrmsg = " registered failed.  Please retry.  If problem persists, please conatact support"
            callbk_proc_data ={
                "typ": "signup",
                "regdata": "401",
                "msg": usrmsg
            }
        else:
            rec_status ="success"
            if usrmsg == None:
                 usrmsg = " registered successfully.  Please reset password before first login"
            callbk_proc_data = {
                "typ": "signup",
                "regdata": "200",
                "msg": nc_email + usrmsg
            }
        
        return  rec_status, callbk_proc_data

def save_usr_details(sav_usr):
    print("inside save_usr_details function")
    s = 0
    f = None
    t = None #message to front end
    rec_status ="fail"

    con, cur, s1, f1 = db.mydbopncon()
    s, f, t = errhand.get_status(s, s1, f, f1, t, "no")
    s1, f1 = 0, None
    print("DB connection established", s,f,t)

    #validate user existence
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
                            """,(uid,sinupadhaar,sinuppan,sinuparn,sinupmobile,sinupemail,entityid,countryid,) )
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
    pan_payload = None

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
                    pan_payload = {"pan": rec['sinuppan']}
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
                    INSERT INTO acusr.userlogin (userid, username, useremail, usertype, userstatus, userstatlstupdt, octime, lmtime, entityid, countryid) 
                    VALUES (%s,%s,%s,'W','A',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,%s,%s);
                    """,(sav_usr["uid"], sav_usr["nc_usrname"], sav_usr["nc_email"],settings.INSTALLDATA[settings.LIVE]["entityid"],settings.INSTALLDATA[settings.LIVE]["countryid"],))
        print(command)

        cur, s1, f1 = db.mydbfunc(con,cur,command)
        s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
        s1, f1 = 0, None

        if s > 0:
            s, f, t= errhand.get_status(s, 200, f, "SIGNUP userlogin insert failed", t, "no")

        print('userlogin Insert or update completed')

    if s <= 0:
        command = cur.mogrify("""
                    INSERT INTO acusr.linkedapps (userid, lnk_entity, lnk_userid, lnk_email, lnk_authtkn, lnk_tknexpiry, lnkstatus, octime, lmtime, entityid, countryid) 
                    VALUES (%s,%s,%s,%s,%s,%s,'L',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,%s,%s);
                    """,(sav_usr["uid"], sav_usr["nc_entity"], sav_usr["nc_usrid"], sav_usr["nc_email"],sav_usr["nc_userauthtkn"],sav_usr["nc_tknexpiry"], settings.INSTALLDATA[settings.LIVE]["entityid"],settings.INSTALLDATA[settings.LIVE]["countryid"],))
        print(command)

        cur, s1, f1 = db.mydbfunc(con,cur,command)
        s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
        s1, f1 = 0, None

        if s > 0:
            s, f, t= errhand.get_status(s, 200, f, "SIGNUP linkedapps insert failed", t, "no")

        print('linked app Insert or update completed')

    if s <= 0:
        con.commit()
        db.mydbcloseall(con,cur)
    
    if s<= 0:
        status = "success"
        msg = "User data saved successfully"
    else:
        status = "fail"
        msg = "User data save failed"
    
    return status, msg