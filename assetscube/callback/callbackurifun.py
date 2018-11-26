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
import jwt

@bp_accallbk.route("/callback",methods=["GET","POST","OPTIONS"])
def callback():
    if request.method=="OPTIONS":
            print("inside callback options")
            response = "inside callback options"
            #print(request.headers)
            response1 = make_response(jsonify(response))            
            return response1

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
        #payload
        #{type: "signup", callbkfrm: "nawalcube", regdata: "a96f2d792641cd049c974e3c9e330f99", msg: "success"}
       
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        entityid = request.headers.get("entityid", None)
        countryid = request.headers.get("countryid", None)
        payload["entityid"] = entityid
        payload["countryid"] = countryid 
        #payload
        #{type: "signup", callbkfrm: "nawalcube", regdata: "a96f2d792641cd049c974e3c9e330f99", msg: "success", "entityid": "ac", countryid: "IN"}
        
        res_status, res_to_send = callback_handler(payload)
        print(res_status, res_to_send)
        if res_status == 'success':
            resps = make_response(jsonify(res_to_send), 200)
            #resps = make_response(jsonify(response), 200 if res_to_send == 'success' else 400)
        else:
            resps = make_response(jsonify(res_to_send), 400)
        
        return resps    

def callback_handler(callback_data):
    #Common handler to handle any callback from oauth
    #callback_data
    #{type: "signup", callbkfrm: "nawalcube", regdata: "a96f2d792641cd049c974e3c9e330f99", msg: "success", "entityid": "ac", countryid: "IN"}

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
    #Common handler to handle any callback from nawalcube
    #callback_data
    #{type: "signup", callbkfrm: "nawalcube", regdata: "a96f2d792641cd049c974e3c9e330f99", msg: "success", "entityid": "ac", countryid: "IN"}

    if callback_data["type"] == "signup":
        return ncclbk_singup_handler(callback_data)
    elif callback_data["type"] == "code":
        return ncclbk_login_handler(callback_data)

def ncclbk_singup_handler(callback_data):
    # handler for nawalcube signup
    #callback_data
    #{type: "signup", callbkfrm: "nawalcube", regdata: "a96f2d792641cd049c974e3c9e330f99", msg: "success", "entityid": "ac", countryid: "IN"}

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
        entityid = callback_data["entityid"]
        countryid = callback_data["countryid"]

        headers = {"entityid": entityid, "countryid": countryid}
        req_payload = {"userauthtkn": callback_data["regdata"], "appid": settings.NCAPPID[settings.LIVE],"appkey":settings.NCAPPKEY[settings.LIVE]}
        print("###########################")
        print(req_payload)
        print(type(req_payload))
        print("###########################")
        r = requests.post(settings.NCSIGNUPDATAFETCHURL[settings.LIVE], headers=headers, data=json.dumps(req_payload))
        nc_usr_data = json.loads(r.content.decode("utf-8") )
        print(json.loads(r.content.decode("utf-8")))
        # Response we get:
        #     Field Name         success                     fail
        # -----------------------------------------------------------
        #  {  
        #    "userauthtkn":  new_userauthtkn,                BLANK
        #     "tknexpiry":   usr_db_rec["tknexpiry"],        BLANK
        #     "userid":      more_usr_db_rec["userid"],      BLANK
        #     "username":    more_usr_db_rec["username"],    BLANK
        #     "emailid":     more_usr_db_rec["sinupemail"],  BLANK
        #     "status":      success                         fail
        #     "msg":         BLANK                           fail message
        #   }
        print('i see')


        if nc_usr_data["status"] == "success":
            nc_email = nc_usr_data["emailid"]
            nc_userauthtkn = nc_usr_data["userauthtkn"]
            nc_tknexpiry = nc_usr_data["tknexpiry"]
            nc_usrid = nc_usr_data["userid"]
            nc_usrname = nc_usr_data["username"]
            uid = None
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
                except auth.AuthError as e:
                    print(str(e.args))
                    s, f, t= errhand.get_status(s, 0, f, ''.join(e.args), t, "no")   
                except Exception as inst:
                    print(inst.args)
                    print(inst)
                    s, f, t= errhand.get_status(s, 0, f, inst, t, "no")
                else:
                    print('Successfully fetched user data: {0}'.format(user.uid))
                    if user.uid != None or user.uid != "":
                        useridex = True
                        uid = user.uid
                    print("user details fetch successful")
                    s, f, t= errhand.get_status(s, 0, f, " email already registered.", t, "no")
                    #usrmsg = "email already registered."
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
                    s, f, t= errhand.get_status(s, 100, f, "User registration failed.  Please cotact support [ac error]", t, "yes")
                except ValueError as e:
                    print("value error while creating user")
                    s, f, t= errhand.get_status(s, 0, f, "Firebase app user details fetch failed", t, "no")
                    s, f, t= errhand.get_status(s, 100, f, "User registration failed.  Please cotact support [ac error]", t, "yes")
                else:
                    print(user.uid)
                    print(format(user))
                    uid = user.uid
            print("inside callback singup success")

        else:
            s, f, t= errhand.get_status(s, 100, f, "User registration failed.<br>  Please contact support [nc fetch].", t, "yes")

        if s <= 0:
            sav_usr = {
                "uid": uid,
                "nc_email" : nc_email,
                "nc_userauthtkn" : nc_userauthtkn,
                "nc_tknexpiry" : nc_tknexpiry,
                "nc_usrid" : nc_usrid,
                "nc_usrname" : nc_usrname,
                "nc_entity": "NAWALCUBE",
                "entityid" : entityid,
                "countryid": countryid
            }
            sav_status, sav_resp_rec = save_usr_details(sav_usr)
            if sav_status != "success":
                print(sav_resp_rec)
                s, f, t= errhand.get_status(s, 100, f, "User registration failed.<br>  Please contact support [ac db update].", t, "yes")

            

        if s <= 0:
            rec_status ="success"
            if usrmsg == None:
                usrmsg = "User registered successfully.  Please reset password before first login"
            else:
                usrmsg = "User registered successfully.  Please reset password before first login. "+ usrmsg
            callbk_proc_data = {
                "typ": "signup",
                "regdata": "200",
                "email" : nc_email,
                "msg": usrmsg
            }
        else:
            rec_status ="fail"
            usrmsg = "Registration failed.   Please retry. <br>  If problem persists, please conatact support"
            callbk_proc_data ={
                "typ": "signup",
                "regdata": "401",
                "email" : nc_email,
                "msg": usrmsg
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
                                SELECT userid, username, useremail, logintype
                                FROM acusr.userlogin
                                WHERE userstatus NOT IN ('I')
                                AND (
                                        userid = %s OR  useremail = %s
                                    )
                                AND entityid = %s AND countryid = %s
                                ) as a
                            """,(sav_usr["uid"],sav_usr["nc_email"],sav_usr["entityid"],sav_usr["countryid"],))
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

        reg_status, reg_data = allow_regis_user(db_json_rec, sav_usr)
        print(reg_status)
        print(reg_data)
        if reg_status == "fail":
            s, f, t= errhand.get_status(s, 101, f, reg_data, t, "yes")
    
    print(s,f)
    
    if s <= 0:
        s1, f1 = db.mydbbegin(con, cur)
        print(s1,f1)

        s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
        s1, f1 = 0, None

    if s <= 0:
        command = cur.mogrify("""
                    INSERT INTO acusr.userlogin (userid, username, useremail, logintype, userstatus, userstatlstupdt, octime, lmtime, entityid, countryid) 
                    VALUES (%s,%s,%s,'I','A',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,%s,%s);
                    """,(sav_usr["uid"], sav_usr["nc_usrname"], sav_usr["nc_email"],settings.INSTALLDATA[settings.LIVE]["entityid"],settings.INSTALLDATA[settings.LIVE]["countryid"],))
        print(command)

        cur, s1, f1 = db.mydbfunc(con,cur,command)
        s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
        s1, f1 = 0, None
        print("end of ")
        if s > 0:
            s, f, t= errhand.get_status(s, 200, f, "SIGNUP userlogin insert failed", t, "no")

        print('userlogin Insert or update completed')

    if s <= 0:
        command = cur.mogrify("""
                    INSERT INTO acusr.linkedapps (userid, lnk_app, lnk_userid, lnk_email,  lnkstatus, octime, lmtime, entityid, countryid) 
                    VALUES (%s,%s,%s,%s,'L',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,%s,%s);
                    """,(sav_usr["uid"], sav_usr["nc_entity"], sav_usr["nc_usrid"], sav_usr["nc_email"],settings.INSTALLDATA[settings.LIVE]["entityid"],settings.INSTALLDATA[settings.LIVE]["countryid"],))
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
        rec_status = "success"
        msg = "User data saved successfully"
    else:
        rec_status = "fail"
        tt = errhand.front_end_msg if errhand.front_end_msg != None else ""
        msg = "User data save failed " + tt
    
    return rec_status, msg


def allow_regis_user(db_json_rec, pyld):
    print("inside allow_regis_user")
    s = 0
    f = None
    t = None #message to front end
    stat = "success"
    usrmsg = None

    if db_json_rec:
        for rec in db_json_rec:
            if rec['userid'] != '':
                if rec['userid'] == pyld["uid"]:
                    s, f, t= errhand.get_status(s, 100, f, "Userid Already exists for the Email id", t, "yes")                  
                    stat = "fail"

            if rec['useremail'] != '':
                if rec['useremail'] == pyld["nc_email"]:
                    s, f, t= errhand.get_status(s, 100, f, "Email Already registered", t, "yes")
                    stat = "fail"
            '''
            if stat != "fail":
                if rec['sinupadhaar'] != '':           
                    if rec['sinupadhaar'] == pyld["sinupadhaar"]:
                        s, f, t= errhand.get_status(s, 100, f, "Adhaar Already registered", t, "no")

                if rec['sinuppan'] != '':
                    if rec['sinuppan'] == pyld["sinuppan"]:
                        s, f, t= errhand.get_status(s, 100, f, "PAN Already registered", t, "no")

                if rec['sinuparn'] != '':                
                    if rec['sinuparn'] == pyld["sinuparn"]:
                        s, f, t= errhand.get_status(s, 100, f, "ARN Already registered", t, "no")

                if rec['sinupmobile'] != '':
                    if rec['sinupmobile'] == pyld["sinupmobile"]:
                        s, f, t= errhand.get_status(s, 100, f, "Mobile Already registered", t, "no")
                
                if s > 0: #incase one of the above already exists
                    if rec["usercusttype"] == pyld["usercusttype"]:
                        s, f, t= errhand.get_status(s, 100, f, "Userid Already exists with same Adhaar/PAN/ARN/MOBILE for selected cust type (ie...Resigter as)", t, "yes")
                        stat = "fail"
            '''
    else:
        print("no records satifying the current user inputs")

    print(pyld)
    print(db_json_rec)

    if stat == "fail":
        usrmsg = errhand.error_msg_reporting(s, t)

    return stat, usrmsg


def ncclbk_login_handler(pyldjson):
    print("inside ncclbk_login_handler function")
    s = 0
    f = None
    t = None #message to front end
    usrmsg = None
    rec_status ="fail"
    callback_data = pyldjson
    print("nc ncclbk_login_handler handler")
    if callback_data["regdata"] == '401':
        # show error page
        print("login handler error")
        callbk_proc_data ={
                "typ": "login",
                "regdata": "401",
                "msg": "Login failed.  Please retry.  If problem persists, please conatact support"
            }        
        return "fail", callbk_proc_data
    else:
        #Get pass token from nawalcube
        data_for_passtkn = {
            "entityid" : callback_data["entityid"],
            "countryid" : callback_data["countryid"],
            "userauthtkn" : callback_data["regdata"]
        }

        status,linked_apps_lst = nc_pass_tkn(data_for_passtkn)
        if status > 0:
             s, f, t = errhand.get_status(s, 200, f, "NC pass token get failed", t, "no")      
      
        if s <= 0:
            rec_status, callbk_proc_data = what_pg_to_show(linked_apps_lst)
          
        if s > 0:
            rec_status = "fail"
            callbk_proc_data = ""

    return  rec_status, callbk_proc_data

def what_pg_to_show(linked_apps_lst):
    #check if any expired pass tokens.  If yes, ask user to login
    #if no create custom token for client to login
    any_exp_tkn = chk_for_expired_tkns(linked_apps_lst)

    if any_exp_tkn == False:
        #All app has valid tokens so allowing app to login
        custom_token = get_custom_token(linked_apps_lst[0]["userid"])
        rec_status = "success"
        callbk_proc_data = {
            "type": "jwt",
            "jwt": custom_token
        }
    else:
        rec_status = "success"
        callbk_proc_data = {
            "type": "applist",
            "apps_list": linked_apps_lst
        }
    
    return rec_status, callbk_proc_data



def chk_for_expired_tkns(linked_apps_lst):
    #Check for any app with expired token
    print("Inside chk_for_expired_tkns")
    print(linked_apps_lst)
    any_exp_tkn = False                
    for lk_app in linked_apps_lst:
        print("******************")
        print(lk_app)
        print("******************")
        if lk_app["pass_tkn_status"] != "active":
            any_exp_tkn = True

    print(any_exp_tkn)
    return any_exp_tkn

def nc_pass_tkn(callback_data):
    #get pass token from nc
    s = 0
    f = None
    t = None #message to front end
    lnkd_app_data = None
    entityid = callback_data["entityid"]
    countryid = callback_data["countryid"]

    headers = {"entityid": entityid, "countryid": countryid}
    req_payload = {
                    "userauthtkn": callback_data["userauthtkn"], 
                    "appid": settings.NCAPPID[settings.LIVE],
                    "appkey":settings.NCAPPKEY[settings.LIVE],
                    "redirecturi":settings.MYREDIRURI[settings.LIVE]
                    }
    print("###########################")
    print(req_payload)
    print(type(req_payload))
    print("###########################")
    #r = requests.post(settings.NCPASSURL[settings.LIVE], headers=headers, data=json.dumps(req_payload))

    try:
        r = requests.post(settings.NCPASSURL[settings.LIVE], headers=headers, data=json.dumps(req_payload))
    except requests.exceptions.Timeout:
        print("timeout exception")
        s, f, t = errhand.get_status(s, 100, f, "Timeout error in sending request to nc", t, "yes")
        #pan_data = {"pan_name": None, "kyc_status": None}
    except requests.exceptions.RequestException as e:
        print("exception")
        print(e)
        s, f, t = errhand.get_status(s, 100, f, "error in sending request to nc", t, "yes")
    else:
        print(r.content)
        nc_usr_data = json.loads(r.content.decode("utf-8") )
        print(json.loads(r.content.decode("utf-8")))
        print('i see')
        print(type(nc_usr_data))
        nc_usr_data = json.loads(nc_usr_data)
        print(nc_usr_data)
        print(type(nc_usr_data))


    jwtdecoded = jwt.decode(nc_usr_data.get("ncjwt"), verify=False)
    print(jwtdecoded)
    ncuid = jwtdecoded["ncuserid"]
    nc_pass_tkn_exp = jwtdecoded["exp"]        

    #Get acuserid from ncuserid
    con, cur, s1, f1 = db.mydbopncon()
    s, f, t = errhand.get_status(s, s1, f, f1, t, "no")
    s1, f1 = 0, None
    print("DB connection established", s,f,t)

    #get acuid from ncuid 
    if s <= 0:
        command = cur.mogrify("""
                                SELECT userid
                                FROM acusr.linkedapps
                                WHERE lnkstatus = 'L'
                                AND lnk_userid = %s
                                AND entityid = %s AND countryid = %s
                            """,(ncuid,entityid,countryid,))
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
        print("rowcount")                
        print(cur.rowcount)
        print("rowcount") 
        if cur.rowcount > 0:
            uid = cur.fetchall()[0][0]
            print(uid)

    print(s,f)
    print("rowcount") 
    
    #Check for other linked apps
    linked_apps_input = {
        "acuid": uid,
        "entityid": entityid,
        "countryid": countryid,
        "pass_tkn_exp" : nc_pass_tkn_exp,
        "pass_tkn": nc_usr_data.get("ncjwt"),
        "lnk_userid": ncuid
    }
    rec_status, linked_apps_lst = get_linked_apps_nd_save(linked_apps_input)
    if rec_status > 0:
        s, f, t = errhand.get_status(s, rec_status, f, "Linked app data fetch failed with error", t, "no")
        print(s,f)

    return s, linked_apps_lst
    


def get_linked_apps_nd_save(linked_apps_input):
    #Get all the linked apps for a acuid
    print("inside get_linked_apps function")
    s = 0
    f = None
    t = None #message to front end
    lnkd_app_data = None

    lnk_passtkn = linked_apps_input["pass_tkn"]
    lnk_pass_exp = datetime.strptime(linked_apps_input["pass_tkn_exp"],'%d%m%Y%H%M%S%f')
    acusrid = linked_apps_input["acuid"]
    lnk_app_uid = linked_apps_input["lnk_userid"]
    entityid = linked_apps_input["entityid"]
    countryid = linked_apps_input["countryid"]

    #Get con and cur
    con, cur, s1, f1 = db.mydbopncon()
    s, f, t = errhand.get_status(s, s1, f, f1, t, "no")
    s1, f1 = 0, None
    print("DB connection established", s,f,t)

    if s <= 0:
        s1, f1 = db.mydbbegin(con, cur)
        print(s1,f1)

        s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
        s1, f1 = 0, None


    if s <= 0:
        command = cur.mogrify("""
                    UPDATE acusr.linkedapps SET lnk_passtkn = %s, lnk_pass_exp = %s
                    WHERE userid = %s AND lnk_userid = %s AND entityid= %s AND countryid = %s;
                    """,(lnk_passtkn, lnk_pass_exp, acusrid, lnk_app_uid, entityid, countryid,))
        print(command)
        cur, s1, f1 = db.mydbfunc(con,cur,command)
        s, f, t= errhand.get_status(s, s1, f, f1, t, "no")
        s1, f1 = 0, None

        if s > 0:
            s, f, t= errhand.get_status(s, 200, f, "SIGNUP update failed", t, "no")

        print('Insert or update is successful')

    if s <= 0:
        con.commit()


    #get the linked apps for the acuid
    #Check for Token expiry of all the apps inside CASE
    if s <= 0:
        command = cur.mogrify("""
                                SELECT json_agg(a) FROM (
                                SELECT *, 
                                    CASE
                                        WHEN (lnk_pass_exp < CURRENT_TIMESTAMP) THEN 'expired' ELSE 'active'
                                    END AS pass_tkn_status
                                FROM acusr.linkedapps
                                WHERE lnkstatus = 'L'
                                AND userid = %s
                                AND entityid = %s AND countryid = %s
                                ) as a
                            """,(linked_apps_input["acuid"],linked_apps_input["entityid"],linked_apps_input["countryid"],))
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
        print("rowcount")                
        print(cur.rowcount)
        print("rowcount") 
        if cur.rowcount > 0:
            lnkd_app_data = cur.fetchall()[0][0]
        else:
            lnkd_app_data = None
    print(lnkd_app_data)
    print(s,f)

    if s <= 0:
        return s, lnkd_app_data
    else:
        return s, lnkd_app_data
 

#def ncapp_auto_auth_processing(lnkd_app_data):
     #Check for Nawalcube app in the linked app list.  
     #If present get authorise token
    

def get_custom_token(uid):
    print("inside get_custom_token function")
    s = 0
    f = None
    t = None #message to front end
    usrmsg = None
    rec_status ="fail"
    #create firebase custom token for users.
    #nc_usr_data
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

    if s <= 0:
        rec_status ="success"
        custom_token = auth.create_custom_token(uid,app=default_app)

    return custom_token.decode("utf-8")