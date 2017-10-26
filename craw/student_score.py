import requests
from bs4 import BeautifulSoup
from craw import simulated_landing

class craw_scorce(object):
    def __init__(self,username,password):
        self.username=username
        self.passowrd=password
        self.headers = {
            'Host': 'jwgl.just.edu.cn:8080',
            'Origin': 'http://jwgl.just.edu.cn:8080',
            'Referer': 'http://jwgl.just.edu.cn:8080/jsxsd/kscj/cjcx_query?Ves632DSdyV=NEW_XSD_XJCJ',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
    def start(self):
        s=simulated_landing.craw.login(self,self.username,self.passowrd)
        response = s.get("http://jwgl.just.edu.cn:8080/jsxsd/kscj/cjcx_list", headers=self.headers)
        response.encoding='utf-8'
        data_list = []
        th_list = ['order_num','start_semester','course_num','course_name','score','credit','total_hours',
                   'examination_method','course_attribute','course_nature','alternative_course_number','alternative_course_name','mark_of_score']
        soup = BeautifulSoup(response.text, "html.parser")
        trs = soup.find_all("tr")[2:]
        for tr in trs:
            tds = tr.find_all("td")
            i = 0
            data = {}
            for td in tds:
                data[th_list[i]] = td.get_text()
                i = i + 1
            data_list.append(data)
        return data_list
if __name__ == '__main__':
    test=craw_scorce("152210702119","935377012pxc")
    print(test.start())
