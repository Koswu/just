import random
import hashlib
import requests


class fanyi(object):
    @staticmethod
    def start(q, fromLang='auto', toLang='auto'):
        url = "http://fanyi-api.baidu.com/api/trans/vip/translate"
        appId = '20171021000089919'
        secretKey = 'ytbSMeuM0wRzV5euPw9O'
        salt = random.randint(32768, 65536)
        sign = appId + q + str(salt) + secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode("utf-8"))
        sign = m1.hexdigest()
        params = {
            'q': q,
            'from': fromLang,
            'to': toLang,
            'appid': appId,
            'salt': salt,
            'sign': sign
        }
        response = requests.post(url, params=params)
        response.encoding = 'utf-8'
        return  response.text
