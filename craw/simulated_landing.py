import requests
class craw(object):
    def __init__(self):
        self.headers = {
            'Host': 'jwgl.just.edu.cn:8080',
            'Origin': 'http://jwgl.just.edu.cn:8080',
            'Referer': 'http://jwgl.just.edu.cn:8080/jsxsd/kscj/cjcx_query?Ves632DSdyV=NEW_XSD_XJCJ',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
    def login(self,username,password):

        if not username or not password:
            return '{"msg":"用户名或者密码为空"}'
        try:
            s = requests.Session()
            form_data = {'USERNAME': username, 'PASSWORD': password}
            s.post("http://jwgl.just.edu.cn:8080/jsxsd/xk/LoginToXk", data=form_data,timeout=10)
            return s
        except Exception  as e:
            return {'msg':'连接失败'}
