# LIVE = 0
# UAT = 1
LIVE = 1

NCAPPID = ['','ce92aa8e9ae4d53acd7ce5eabca48f02fe556a7cee346c2c233ff3c2e570048c']
NCREGURL = ['','http://localhost:8080/ncappsignup']
MYHOMEPG = ['','http://localhost:4201']
MYREDIRURI = ['','http://localhost:8081/callback']

FBSERVICEAC = {
  "type": "service_account",
  "project_id": "ananew-472d8",
  "private_key_id": "3cc49b4d740c111a64af75a930a6488b3233b3d8",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC/EyWjBWv9wmAL\nwX8BP2kfDyDxC5EvET3S/ENY8clbb8FXb/8HfC0LWruCg+50EcTV6lIwKPTa+rzC\ni6V5yqsFqpOSC3TrrqF2dr/TEHK5+1KDS/i45QsuRfM9tHcJCI2vZUYHIFQb0cpT\nUZ2hi4DSf5ci5OQUhyxM9eeJSY0X/KYfe4uddT0nTUAIh2qRyLiBvECHRjXCcqVO\nPyEQIgfgwAiZH5oXEPCvyvdy4XfyE2/bd9+J/gSPohfya2WyQzGA2luRYZjdYXFo\n936Q3DMuCxUkj3pd+APZX3Q5zzKAI7G1kZeAoT/NKRX5CxhXXWgQSQZef6wUkkOL\n2SHGl6Z7AgMBAAECggEAAvZbpIVwRpBi9dEIG4vmZ+8k8cQzT06qZsSakSPzZCx2\nNmeL07ZFFS0mNy6hAUjkkp5zOhXOsSBuJxXFDkab8LpFc4rOfBS1MHdEg0yxtG3l\nHcM37skE8r7gG0Mv8QmiTLWsTBk1fYEliQsLDcGAbYMIjos26rHkPzbDN5YPgKhl\nZ/UyH5PIOL84rZea0BCbmsvmDmEeLQ5U5z1TYwsQn9Yn/q7Qc9mVRaoLkf8Wp4NS\njDdgpgOmH9LP/GOa09GZ8a88hXTwLwg/OK8XuQiuxG8M+/3HqiY5ps1tZNQnzdCf\n5IBFdM/DKBeuEx5ijVHWL2sdstSZ03Ss24watVPwPQKBgQDekMguSk0CBaQumQsb\nGlmfWhJtYFDoXEecc/Qzxd+2BbwZywLXnIf8lb7v/omiNarZRjs4BSPozblzzvUo\nlldso+IX/fAMRzuvhud88JU5Ti6jJ4Ih3diwAUcSoNKmfei1nyIfdL8cdZlkACpS\nvyTWeK7FxXNopSxrw1eZK6zt5QKBgQDbx1Kirv2Psmw51lLm3NLitv8tNkFvSQJo\n/1s3U+pb/I14/KHQS3dpc0j1AmCoRkokc6JBEhTnqm/ZUfd3BZzpMtdDFFCJIvc1\nMp92So1u+d9OsLMCNbYlA/xH48M8W0InttG99Pv/2l3ysPgXNFIrO/usYMIw+OF8\n2wGaKTv83wKBgD0ouemGf1zT4gbwBU5AUmponPGzaug/G2qRroRflpb1QngwAirv\nl6rAF4TphDav2q/0DafaOcDqb1C0iUfK8GEpM6L2I/WryWn1fz0k+0yRAF3TKH5X\n8QiEgVxMFzarGLx36y+LrEyMwEbriLXOUrgg153/ITSbVvaR6ktr5gxFAoGAd6t3\n1ndcP7NSdMe7ylMxTRuBpLenN5ZUhqGMpHq/4KiKy/cbkNSWx8drUWWjBd2IH4ML\nNU1ILsDCOF4GVjurLdtuFOtp0tJEMyZGZ92+V1AdhLZ4MlrWvB8IboiZVTMHuaI1\nYK6VzMG1aCFuZQwrNblql3j0JEBQX3DM1YlgTZcCgYEAvAPjKhJQlwExP1W56IgJ\nlzOAcw19TeXk94A+T3kNX+Wx+ItkAUh4OYtwXQXrrG0jYpKvQ1tGk22ZY5T4Frdc\nMMi5w8JlyIJqmCidaQz5GGaM2MIgsyrDD6vPHtEI4hUMg67X5mQV4sf7F5VZijie\nTfnQIyZCcUSEzHsW3L5570s=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-g6qg2@ananew-472d8.iam.gserviceaccount.com",
  "client_id": "102124765773320469248",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-g6qg2%40ananew-472d8.iam.gserviceaccount.com"
}

# gunicorn --reload --bind=127.0.0.1:8081 assetscube:app