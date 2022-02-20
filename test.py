# 测试TT识图
from PIL import Image
import os
from cv2 import imshow
import requests
import time
from io import BytesIO
import random
import matplotlib.pyplot as plt
from alive_progress import alive_bar
import base64
import json

ELECTIVE_XH = input("id:")
ELECTIVE_PW = input("pwd")
DELAY_S_MIN = 1.5
DELAY_S_DELTA = 1.5
ITERS = 100
PATH = os.path.dirname(__file__)
tt_usr = input("tt_usr")
tt_pwd = input("tt_pwd")

# adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, pool_block=True)
s = requests.Session()
# s.mount('http://elective.pku.edu.cn', adapter)
# s.mount('https://elective.pku.edu.cn', adapter)

def login():
    print('login')
    res = s.post(
        'https://iaaa.pku.edu.cn/iaaa/oauthlogin.do',
        data={
            'appid': 'syllabus',
            'userName': ELECTIVE_XH,
            'password': ELECTIVE_PW,
            'randCode': '',
            'smsCode': '',
            'otpCode': '',
            'redirUrl': 'http://elective.pku.edu.cn:80/elective2008/ssoLogin.do'
        },
    )
    res.raise_for_status()

    json = res.json()
    assert json['success'], json
    token = json['token']

    res = s.get(
        'https://elective.pku.edu.cn/elective2008/ssoLogin.do',
        params={
            'rand': '%.10f'%random.random(),
            'token': token,
        },
    )
    res.raise_for_status()

def get_captcha():

    res = s.get(
        'https://elective.pku.edu.cn/elective2008/DrawServlet?Rand=123456',
        headers={
            'referer': 'https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            #'cookie': ELECTIVE_COOKIE,
        },
        timeout=(3,3),
    )

    res.raise_for_status()
    rawim = res.content

    # if not rawim.startswith(b'GIF89a'):
    #     print(res.text)
    #     raise RuntimeError('bad captcha')

    return rawim

def check_captcha(captcha):

    res = s.post(
        'https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/validate.do',
        headers={
            'referer': 'https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/SupplyCancel.do',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            #'cookie': ELECTIVE_COOKIE,
        },
        data={
            'xh': ELECTIVE_XH,
            'validCode': captcha,
        },
        timeout=(3,3),
    )
    res.raise_for_status()
    try:
        json = res.json()
    except Exception as e:
        if '异常刷新' in res.text:
            login()
            return check_captcha(captcha)
        else:
            print(res.text)
            raise

    if json['valid']!='2':
        return False
    else:
        return True

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


if __name__ == '__main__':


    login()
    time.sleep(0.5)

    right = 0

    with alive_bar(ITERS) as bar:
        for i in range(ITERS):

            bar()
            res = get_captcha()
            im = Image.open(BytesIO(res))
            # plt.imshow(im)
            # plt.show()
            img_path = os.path.join(PATH,f'captcha/{i+1}.jpg')
            im.save(img_path)

            ret, text  = base64_api(uname=tt_usr, pwd=tt_pwd, img=img_path, typeid=1003)# 3(数英混合) 1003(数英混合2) 7(无感学习)

            if ret:
                print("CAPTCHA: ",text,end="")
                correct = check_captcha(text)
                if correct: 
                    right += 1
                    print(" √",end="")
            else:
                print("ERROR: ",text,end="")

            print()
            time.sleep(0.01)

    print(f"accuracy: {right/ITERS*100}%")
        
