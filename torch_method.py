#本文件为验证码识别api（TT识图）
import base64
import json
import requests



def base64_api(uname, pwd, img, typeid):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)

    if result['success']:
        return True , result["data"]["result"]
    else:
        return False, result["message"]



