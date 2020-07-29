import requests
from bs4 import BeautifulSoup as bs
import time

class Pixiv():
    def __init__(self, path = "./imgs/craw/pic", pixiv_id = "", password = ""):
        self.url = "https://www.pixiv.net"
        self.path = path
        self.head = {
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36" ,
            "referer" : self.url
        }
        self.postdata = {
            'pixiv_id': pixiv_id,
            'pass': password
        }

        self.req = None
    
    def change_path(self, path):
        self.path = path

    def change_loggin(self, pixiv_id, password):
        self.postdata['pixiv_id'] = pixiv_id
        self.postdata['pass'] = password

    def get_pic(self, locate, tags = []):
        '''give the website or the number of the pic, 
            if the tags are included in pic tags,
            then will dl the pic. '''
            
        pic_tags = set()

        try:
            int(locate)
            url = self.url + '/artworks/' + str(locate)
        except:
            url = str(locate)
        
        title = url[-8:]
        req_page = requests.get(url)
        self.head["referer"] = url
        soup_page = bs(req_page.text,"html.parser")
        sel_page = soup_page.select("meta#meta-preload-data")
        
        

        if sel_page:
            for pic_info in sel_page[0]["content"].split(","):
                if "regular" in pic_info:
                    url_front_pic = pic_info[11:-17]
                    url_back_pic = pic_info[-16:-1]
                if "tag" in pic_info and "{" in pic_info:
                    pic_tags.add(pic_info.lstrip('tagsauthorId":[{')[:-1])
        
        i = 0
        do = True
        
        for tag in tags:
            if not tag in pic_tags:
                do = False

        req_pic = requests.get(url_front_pic + str(i) + url_back_pic, headers = self.head)
                
        while do and ("403 Forbidden" and "404 Not Found" not in req_pic.text):       
            img = req_pic.content
            
            if (i == 0):
                filename = title +'.png'
            else:
                filename = title + '(' + str(i) + ')' + '.png'
            
            with open (self.path + '/' + filename , 'wb') as f:
                f.write(img)
            
            i = i + 1
            req_pic = requests.get(url_front_pic + str(i) + url_back_pic, headers = self.head)

        self.head["referer"] = self.url

    def run_rank(self, mode = None, content = None, date = None, tags = []):
        '''dl pic on the rank. now can only dl for one page'''
        url = self.url + "/ranking.php"
        params = {'mode' : mode , 'content' : content , 'date' : date}

        req_rank = requests.get(url, params = params)
        soup_rank = bs(req_rank.text,"html.parser")
        sel_rank = soup_rank.select("div.ranking-image-item a")

        hr_rank = []
        for s in sel_rank:
            hr_rank.append(s["href"])

        for hr in hr_rank:
            if '/artworks/' in hr:
                locate = hr[-8:]
                #print(hr)
                self.get_pic(locate, tags)
                time.sleep(1)

if __name__ == '__main__':
    p = Pixiv()
    p.get_pic(83113557, ['魔法少女まどか☆マギカ','鹿目まどか'])
    #p.run_rank(date = 20200725)

            

        

