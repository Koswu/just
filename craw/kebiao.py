import requests
from bs4 import BeautifulSoup
from craw import simulated_landing
import pandas
class craw_kebiao(object):
    def __init__(self,username,password,semester,week):
        self.usernmae=username
        self.password=password
        self.week=week
        self.semester=semester
        self.session=simulated_landing.craw.login(self,self.usernmae,self.password)
    def start(self):
        data_list=[]
        url = "http://jwgl.just.edu.cn:8080/jsxsd/xskb/xskb_list.do"
        paramrs = {'zc': self.week, 'xnxq01id':self.semester}
        response =self.session.get(url, params=paramrs)
        response.encoding = 'utf-8'
        soup=BeautifulSoup(response.text,"html.parser")
        trs=soup.select("#kbtable tr")
        del trs[0]
        del trs[5]
        week_list=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        for tr in trs:
            data={}
            tds=tr.select(".kbcontent")
            for i,td in enumerate(tds):
                data[week_list[i]]=tds[i].get_text()
            data_list.append(data)
        print(data_list)
        # df=pandas.DataFrame(data_list)
        # df.to_html(r"E:\kebiao.html")
        return  data_list

if __name__ == '__main__':
    c=craw_kebiao("152210702119","935377012pxc",'2016-2017-2','2')
    c.start()
