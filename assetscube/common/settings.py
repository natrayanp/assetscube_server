# LIVE = 0
# UAT = 1
LIVE = 1

NCAPPID = ['','501423418772fe69f94def7239c597659838247c548b2d371ff86501240c7282']
NCAPPKEY = ['','e4eff02aba5aff21b37afd86494953d7']
NCREGURL = ['','http://localhost:8080/ncappsignup']
NCLOGINURL = ['','http://localhost:4200/authorise/auth']
NCSIGNUPDATAFETCHURL = ['','http://localhost:8080/ncappfetchfrmtkn']
MYHOMEPG = ['','http://localhost:4201']
MYREDIRURI = ['','http://localhost:4201/noti/nc']
MYNOTIPG = ["","http://localhost:4201/noti"]

FBSERVICEAC = {
  "type": "service_account",
  "project_id": "natauth-c532d",
  "private_key_id": "b6488f8cafa96101a8a9bf2eb70284886f1a6b64",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDNDI43ap2RctZ/\nKBztrrA9amBI4h0ICJpBC5wgA3Cqsv9oQ1AwwA352EvdzC1IHqURniGtolBklLxJ\nW6tfmRGtKKMuRIrXZWZPowjeyK79BIcpCvTRqExLaBMUwFhfe2JoDnGl2T6pxt4N\nW9FiF8y+jr2Yo2iBSjM+DxFVFeAn5GusdtNtral83R8pvJPaXzR0ERHn7xwwLBa/\nVWWyNLaO8ISkJz2s6oQFFjZIsmy1ZduU7ZdDNdai+JEaWYGRqDmTPi8ncqTPsSF8\ndFnpiZ2+zOib4FPHCXi16AMgB64rUf3Izo8RgKyODfCv86t00DojBVVRv6qvTPTp\n6kWgfXbfAgMBAAECggEAEwakN44j+rf+ISRWstMvtTMmpfydFv69WWW7YdkP3jbn\nrgP4790SLumb+IOWfAej52OV2meiMAMBCYmA+EjatAd+RK/FdkEJYkBNdWaHniCK\nbgt/Nej401Jf2uASEyH+uosEjo/+2YADYJfxcLmmnNPf0cbvzndVE+AQCqYR+4Fy\n2OCL8KvCaKQWf41y9oSVWnjl3vLrPYwsQGJtNoLINkHriG/Q2N74Gc7FD3cEe0GC\nib9xJGUjbmBOOqmm3Aen2/YNn/e34p9GraehfG7iUujClyvL8e+r4Tyh9hXWZAA+\nnKAn7g8fVVwthKBxs6MaIy1V1O8Sd1Ub1XXEooJTgQKBgQDqSCtMdfIcblZlVL5m\nGTX6vwd/C1fCNlB3hSfp8spD+JTFcaaSDExo7P0Z8UUJXGZy1u088k0TzZs3ouRj\n8BONhyZ5ZuXjogvb11XDPEmchCBb6AuW/RztgWLwm2jKWI0+YfitbKH4PmaVzp9X\n3uCI6t3BUhVUArlyX3DUJAyqQQKBgQDgDqaCaXPwOTw0u3EAVPH/cNPXfQluFFIC\nzvd8+KCuk2fsDyAVunlFXslhyzyOZxnbB0DaIisSwax4CAc3k8A010NMlvE1GlDP\nZMe72M5kQNEcroKkC9L0qlTchIuBMZbgdFEUcpoxnhp/xD20tAC1oL/DY90M29QU\n71vYHDSZHwKBgQDgT9EFGDiDeDFIO+dAogrI1XY78YRI8vAAP4GDwW5fvfXTRYmS\ndCwEmkOLPzI2UD3W3mmu3N9ngoiGsHO0K/zMmQYBXr/lPxXTm00F7Qcd0HObC4Vt\nP1MfI66zaFjgxAAYJn2OrmA16qkV7gsqer7I2PcRTaIWGbWtCCxjMVDfAQKBgQC3\nQQRLMbjTx9xIPO7FmLR9emipnOjzkccp6OFe43N4lbOvzQcu/l9lr4sCY1naFtV8\n4UfXoY6dPq6zVc2hVUUlctLmd6Y9CpMBran3J/JW6PSfgtPzHICkABR8cCQxvL9s\nQXZ3ROx8nJWL3pOhkn/qDdoKE0me1MV3gfYaoacbfQKBgQDjaB9D5n/qFRnJAyx1\n47CD9Sl9LLT+kjMH7njNFf9G94V1PqdqwJCM25EmubLydJUHgKKV8CVrnI2dft4o\nOzLdLCiHOyIQQkh5k/HGOLZNW3EvVAXzrBB421G5+/R5mh4+2DkXGEDJtkaC9lyX\nA8RqACQsKdNaw4r1qhQ9owZJow==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-spvoh@natauth-c532d.iam.gserviceaccount.com",
  "client_id": "113492014710780237016",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-spvoh%40natauth-c532d.iam.gserviceaccount.com"
}

INSTALLDATA = [{},
{
    "entityid": "ASSETSCUBE",
    "countryid": "IN"
}]

# gunicorn --reload --bind=127.0.0.1:8081 assetscube:app