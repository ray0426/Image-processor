import requests
from bs4 import BeautifulSoup as bs
import json
import time

class Picture():
    '''use for recording data about the pic on the website'''
    def __init__(self, url = ""):
        '''give url and record data'''
        self.pic = url[-8:]
        self.page = "p0"
        self.title = ""
        self.painter = ""
        self.place = ""
        self.tag = []
        self.paint_time = ""
        self.download_time = ""

        if url:
            req = requests.get(url)
            if ("403 Forbidden" and "404 Not Found" not in req.text):
                soup = bs(req.text,"html.parser")
                self.setting(soup)
            self.get_info('easy')
        
    def get_info(self, mode = 'all'):
        if self.place:
            if mode == 'all':
                print("pic",self.pic)
                print("title:",self.title)
                print("painter:",self.painter)
                print("place:",self.place)
                print("tag:",self.tag)
                print("paint_time",self.paint_time)
                print("download_time",self.download_time)
                print("")
            if mode == 'easy':
                print("pic",self.pic)
                print("title:",self.title)
                print("")
        else: print("something wrong")
    
    def copy(self,copypic):
        self.pic = copypic.pic
        self.page = copypic.page
        self.title = copypic.title
        self.painter = copypic.painter
        self.place = copypic.place
        self.tag = copypic.tag
        self.paint_time = copypic.paint_time
        self.download_time = copypic.download_time

    def is_empty(self):
        if not self.place:
            return True
    
    def setting(self, soup):
        self.set_title(soup)
        self.set_painter(soup)
        self.set_place(soup)
        self.set_tag(soup)
        self.set_paint_time(soup)
        self.set_download_time(soup)

    def set_title(self, soup):
        self.title = soup.title.string[1:-8]
        
    def set_painter(self, soup):
        self.painter = ""
        sel = soup.select("meta#meta-preload-data")
        if sel:
            for s in sel[0]["content"].split(','):
                if ("authorId" in s):
                    painter_id = s.lstrip('tags":[{authorId')[:-1]
                if ("userName" in s):
                    self.painter = s[12:-2]
                if self.painter:
                    break
            self.painter = self.painter + "(id:" + painter_id + ")"

    def set_place(self, soup):
        sel = soup.select("meta#meta-preload-data")
        if sel:
            for s in sel[0]["content"].split(','):
                if "regular" in s:
                    self.place = s[11:-1]
                    break

    def set_tag(self, soup):
        sel = soup.select("meta#meta-preload-data")
        if sel:
            for s in sel[0]["content"].split(','):
                if ("tag" in s and "{" in s):
                    self.tag.append(s.lstrip('tags":[{authorId')[:-1])
    
    def set_paint_time(self, soup):
        sel = soup.select("meta#meta-preload-data")
        if sel:
            for s in sel[0]["content"].split(','):
                if ("uploadDate" in s):
                    self.paint_time = s[14:-7]
    
    def set_download_time(self, soup):        
        self.download_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()) 

    def set_page(self, page):
        self.page = "p" + str(page)

class Pixiv():
    '''use for crawing on Pixiv'''
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
        self.info = dict()
    
    def change_path(self, path):
        self.path = path

    def change_loggin(self, pixiv_id, password):
        self.postdata['pixiv_id'] = pixiv_id
        self.postdata['pass'] = password

    def set_pic_info(self, pic):
        picname = pic.pic 
        picpage = pic.page
        key = picname + "_" + picpage
        self.info[key] = pic
        return key

    def get_pic(self, locate, tags = []):
        '''give the website or the number of the pic, 
            if the tags are included in pic tags,
            then will dl the pic. '''

        try:
            int(locate)
            url = self.url + '/artworks/' + str(locate)
        except:
            url = str(locate)
        
        self.head["referer"] = url

        pic = Picture(url)
        picname = self.set_pic_info(pic)             
        url_front_pic = pic.place[:-16]
        url_back_pic = pic.place[-15:]

        i = 0
        do = True
        
        for tag in tags:
            if not tag in pic.tag:
                do = False

        req_pic = requests.get(url_front_pic + str(i) + url_back_pic, headers = self.head)
                
        while do and ("403 Forbidden" and "404 Not Found" not in req_pic.text):       
            img = req_pic.content
            
            filename = picname +'.png'            
            with open (self.path + '/' + filename , 'wb') as f:
                f.write(img)
            
            i = i + 1

            pic_else = Picture()
            pic_else.copy(pic)
            pic_else.set_page(i)
            picname = self.set_pic_info(pic_else)

            req_pic = requests.get(url_front_pic + str(i) + url_back_pic, headers = self.head)
            
        del self.info[picname]
        print("for", i ,"pages")
        print("")

        self.head["referer"] = self.url

#    def run_rank_old(self, mode = None, content = None, date = None, tags = []):
#        '''dl pic on the rank. now can only dl for one page'''
#        url = self.url + "/ranking.php"
#        params = {'mode' : mode , 'content' : content , 'date' : date}
#
#        req_rank = requests.get(url, params = params)
#        soup_rank = bs(req_rank.text,"html.parser")
#        sel_rank = soup_rank.select("div.ranking-image-item a")
#
#        hr_rank = []
#        for s in sel_rank:
#            hr_rank.append(s["href"])
#
#        for hr in hr_rank:
#            if '/artworks/' in hr:
#                locate = hr[-8:]
#                #print(hr)
#                self.get_pic(locate, tags)
#                time.sleep(1)
    
    def run_rank(self, mode = None, content = None, date = None, tags = [], page = float('inf'), limit = float('inf')):
        '''dl pic on the rank.
            page : dl for how many pages
            limit : dl for how many pic'''
        url = self.url + "/ranking.php"
        params = {'mode' : mode , 'content' : content , 'date' : date, 'format' : 'json'}

        hr_rank = []
        i = 0
        p = 1
        
        while p <= page and i < limit:
            params['p'] = str(p)

            try:
                req_rank = requests.get(url, params = params)
            except:
                if p == 1 :
                    print("maybe your params have wrong keyword")
                else :
                    print("something unknown happened")
                break

            js_rank = json.loads(req_rank.text)
            
            for ele in js_rank['contents']:
                if i < limit:
                    hr_rank.append(ele['url'][-26:-18])
                i = i + 1
            p = p + 1

        for hr in hr_rank:
            try:
                num_hr = int(hr)
                self.get_pic(num_hr ,tags = tags)
                time.sleep(1)
            except:
                print("we got wrong url %s", hr)

if __name__ == '__main__':
    p = Pixiv()
    #p.get_pic(83113557, ["魔法少女まどか☆マギカ","星空ドレス"])
    p.run_rank(date = 20200725, limit = 3)
    print(p.info)

            

        

