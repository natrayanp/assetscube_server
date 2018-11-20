# LIVE = 0
# UAT = 1
LIVE = 1

NCAPPID = ['','']
NCAPPKEY = ['','']
NCREGURL = ['','']
NCLOGINURL = ['','']
NCSIGNUPDATAFETCHURL = ['','']
NCPASSURL = ['','']
MYHOMEPG = ['','http://localhost:4201']
MYREDIRURI = ['','http://localhost:4201/noti/nc']
MYNOTIPG = ["","http://localhost:4201/noti"]
AUTOAUTHAPPS = [[],["NAWALCUBE"]]

FBSERVICEAC = {

}

INSTALLDATA = [{},
{
    "entityid": "ASSETSCUBE",
    "countryid": "IN"
}]

# gunicorn --reload --bind=127.0.0.1:8081 ac:app