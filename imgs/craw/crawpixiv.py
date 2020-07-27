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

    def get_pic(self, locate):
        '''give the website or the number of the pic, will dl the pic(first pic only now)'''
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
        
        i = 0

        for pic in sel_page:
            for pic_info in pic["content"].split(","):
                if "regular" in pic_info:
                    req_pic = requests.get(pic_info[11:-1] , headers = self.head)
                    img = req_pic.content

                    if (i == 0):
                        filename = title +'.png'
                    else:
                        filename = title + '(' + str(i) + ')' + '.png'

                    with open (self.path + '/' + filename , 'wb') as f:
                        f.write(img)
                    break
            i = i + 1

        self.head["referer"] = self.url

    def run_rank(self, mode = None, content = None, date = None, tag = None):
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
                self.get_pic(locate)
                time.sleep(1)

if __name__ == '__main__':
    p = Pixiv()
    #p.get_pic(83182630)
    p.run_rank(date = 20200725)

            

        

