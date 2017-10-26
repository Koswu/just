import requests
from bs4 import BeautifulSoup

class Proxy():
    def __init__(self):
        MAX=5
        self.headers={
            "Host":"moment.douban.com",
            "Referer":"https://moment.douban.com/app/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Proxy-Connection":"keep-alive"
        }

    def getPage(self,url):
        FAILTIME=0
        try:
            result=requests.get(url,headers=self.headers)
            result.encoding="utf-8"
            return result
        except:
            FAILTIME+=1
            if FAILTIME==self.MAX:
                print("发生错误")
                return ''

class Photo():
    def __init__(self):
        self.photo_list=[]
        self.photo_json={}

    def get_photo(self):
        p=Proxy()
        result=p.getPage("https://moment.douban.com/app/")
        soup=BeautifulSoup(result.content,'html.parser')
        li_list=soup.find('div', attrs={'id': 'selection'}).find_all("li")
        photo_title=li_list[2].find('h3').text #图片主题
        photo_url=li_list[2].find('a').get('href')#图片详情界面url

        result1=p.getPage(photo_url)
        soup=BeautifulSoup(result1.content,"html.parser")
        photo_introduction=soup.find('div', attrs={'id': 'content'}).find("p").text
        self.photo_json["title"]=photo_title
        self.photo_json["introduction"]=photo_introduction
        temp_list=soup.find_all('div', attrs={'class': 'content_img'})
        for i in temp_list:
            self.photo_list.append(i.find("img").get("src"))
        num=0
        for j in self.photo_list:
            num+=1
            self.photo_json['photo'+str(num)]=j
        return self.photo_json

class Food():
    def __init__(self):
        self.food_list=[]
        self.food_json={}

    def get_food(self):
        p = Proxy()
        result = p.getPage("https://moment.douban.com/app/")
        soup = BeautifulSoup(result.content, 'html.parser')
        li_list = soup.find('div', attrs={'id': 'selection'}).find_all("li")
        food_title = li_list[6].find('h3').text  # 食物标题
        self.food_json['title']=food_title
        food_url = li_list[6].find('a').get('href')  # 食物详情界面url
        result1 = p.getPage(food_url)
        soup = BeautifulSoup(result1.content, "html.parser")
        father=soup.find('div', attrs={'id': 'content'})
        for child in father.children:
            if 'img'not in str(child):
                self.food_list.append(child.text)
            else:
                self.food_list.append(child.find("img").get('src'))
        num=0
        for i in self.food_list:
            num+=1
            self.food_json["content"+str(num)]=i
        return self.food_json




