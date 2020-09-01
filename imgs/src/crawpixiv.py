import requests
from bs4 import BeautifulSoup as bs
import json
import time
import os
import numpy as np
from tag_data import Img_Tag as Tag
from img_data import Img_Data as Img


class Picture():
    '''use for recording data about the pic on the website'''
    def __init__(self, url = "", path = "./pixiv", detail = dict()):
        '''give url and record data'''
        self.pic = url[-8:]
        self.page = "p0"
        self.title = ""
        self.painter = ""
        self.painter_id = ""
        self.place = ""
        self.tag = []
        self.paint_time = ""
        self.download_time = ""
        self.path = path
        self.detail = detail
        self.need_record = True

        if url:
            req = requests.get(url)
            if ("403 Forbidden" and "404 Not Found" not in req.text):
                soup = bs(req.text,"html.parser")
                self.setting(soup)
            self.get_info('easy')

    def dict_type(self):
        info = {
            "img_ID": self.pic,
            "page": self.page,
            "painter":self.painter,
            "painter_ID": self.painter_id,
            "src": self.path + "/" + self.pic + "_" + self.page + ".png",
            "format": "png",
            "url": self.place,
            "title": self.title,
            "tags": self.tag,
            "paint_time": self.paint_time,
            "download_time": self.download_time
        }
        
        for key, ele in self.detail.items():
            info[key] = ele
        print(info)
        return info

    def get_info(self, mode = 'all'):
        if self.place:
            if mode == 'all':
                print("pic",self.pic," ",self.page)
                print("title:",self.title)
                print("painter:",self.painter)
                print("place:",self.place)
                print("tag:",self.tag)
                print("paint_time",self.paint_time)
                print("download_time",self.download_time)
                print("path",self.path)
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
        self.path = copypic.path

    def is_empty(self):
        if not self.place:
            return True
    
    def setting(self, soup):
        self.set_title(soup)
        self.set_painter(soup)
        self.set_place(soup)
        self.set_tag(soup)
        self.set_paint_time(soup)
        self.set_download_time()

    def set_title(self, soup):
        self.title = soup.title.string[1:-8]
        
    def set_painter(self, soup):
        self.painter = ""
        sel = soup.select("meta#meta-preload-data")
        if sel:
            for s in sel[0]["content"].split(','):
                if ("authorId" in s):
                    self.painter_id = s.lstrip('tags":[{authorId')[:-1]
                if ("userName" in s):
                    self.painter = s[12:-2]
                if self.painter:
                    break

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
    
    def set_download_time(self):        
        self.download_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()) 

    def set_page(self, page):
        self.page = "p" + str(page)

    def set_path(self, path):
        self.path = path

    def set_detail(self, detail):
        for key, ele in detail.items:
            self.detail[key] = ele

    def add_tag(self, tags):
        self.tag.extend(tags)

class Pixiv():
    '''use for crawing on Pixiv'''
    def __init__(self, path = "./pixiv", pixiv_id = "", password = "", mode = 0):
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

        self.req = None     #now request website, use for referer
        self.info = dict()  #put class Picture in it
        
        self.tag = Tag()    #Tag class
        self.tag.load_tags()

        self.db = Img()

        self.mode = mode
        self.mode_we_have = {
            0 : "get_pic_then_save" ,
            1 : "call_then_save" ,
            2 : "task_fin_save"
        }
        self.mode_depend = ["load save"]
        self.work_list = np.zeros((len(self.mode_we_have) , len(self.mode_depend)))
        self.mode_setting()

        print("pixiv set successfully\n\n")
        #usage : self.work_list

#mode part
    def get_mode(self):
        print("current mode",self.mode)
        print("the modes")
        print(self.mode_we_have)
        print()
        print(self.mode_depend)
        print(self.work_list)

    def mode_setting(self): 
        self.work_list[0][0] = 1

#changing part
    def change_mode(self, mode):
        if (mode in self.mode_we_have):
            self.mode = mode
        else:
            print("no such type")

    def change_path(self, path):
        self.path = path

    def change_loggin(self, pixiv_id, password):
        self.postdata['pixiv_id'] = pixiv_id
        self.postdata['pass'] = password
#partial functions for get pic
    def next_page(self, picname, i):
        """give i+1, return i+n where i+n isn't loaded before"""
        while self.db.Search(picname[:-3], 'p' + str(i)):
            print("page", i ,"already load")
            int(i)
            i += 1
        return i

    def trans_number(self, locate):
        try:
            int(locate)
            url = self.url + '/artworks/' + str(locate)
        except:
            url = str(locate)

        return url

    def get_pic_name(self, pic):
        picname = pic.pic 
        picpage = pic.page
        name = picname + "_" + picpage
        #self.info[key] = pic
        return name
#write in json
    def writetag(self, pics):
        for pic in pics:
            pic.tag = self.tag.tags_to_id(pic.tag)
            # write in json data pool?
        self.tag.write_tags()

    def writeinfo(self):
        for pic in self.info.values():
            if pic.need_record:
                self.db.data_add(pic.dict_type())
                pic.need_record = False

        self.db.write_data()

#get pic part
    def get_pic(self, locate, tags = []):
        '''give the website or the number of the pic, 
            if the tags are included in pic tags,
            then will dl the pic. '''

        url = self.trans_number(locate)
        
        self.head["referer"] = url

        pic = []
        pic.append(Picture(url,self.path)) 
        picname = self.get_pic_name(pic[-1])             
        url_front_pic = pic[-1].place[:-16]
        url_back_pic = pic[-1].place[-15:]

        i = self.next_page(picname, 0)
        #print(i)
        do = True
        
        for tag in tags:
            if not tag in pic[-1].tag:
                do = False

        req_pic = requests.get(url_front_pic + str(i) + url_back_pic, headers = self.head)
                
        while do and ("403 Forbidden" and "404 Not Found" not in req_pic.text):
            self.info[picname] = pic[-1]   #add new info
            img = req_pic.content
            filename = picname +'.png'            
            with open (self.path + '/' + filename , 'wb') as f:     #dl pic
                f.write(img)
            
            i = self.next_page(picname, i + 1)
            #print(i)
            pic_buffer = Picture()
            pic_buffer.copy(pic[-1])
            pic_buffer.set_page(i)
            pic_buffer.set_download_time()
            pic.append(pic_buffer)     #next page

            picname = self.get_pic_name(pic[-1])
            req_pic = requests.get(url_front_pic + str(i) + url_back_pic, headers = self.head)
            #change data

        print("for", i ,"pages")
        print("")

        self.writetag(pic)
        if self.work_list[self.mode][0]:
            self.writeinfo()

        self.head["referer"] = self.url
    
    def run_list(self, piclist, tags = []):
        for hr in piclist:
            print(hr)
            try:
                num_hr = int(hr)
                self.get_pic(num_hr ,tags = tags)
                time.sleep(1)
            except:
                print("we got wrong url", hr)

    def run_rank(self, tags = [], mode = None, content = None, date = None, limit = float('inf')):
        '''dl pic on the rank.
            page : dl for how many pages
            limit : dl for how many pic'''
        url = self.url + "/ranking.php"
        params = {'mode' : mode , 'content' : content , 'date' : date, 'format' : 'json'}

        hr_rank = []
        i = 0
        p = 1
        
        while i < limit:
            params['p'] = str(p)

            try:
                req_rank = requests.get(url, params = params)
            except:
                if p == '1' :
                    print("maybe your params have wrong keyword")
                else :
                    print("something unknown happened")
                break

            js_rank = json.loads(req_rank.text)
            #print(js_rank)
            
            for ele in js_rank['contents']:
                #print(ele)
                if i < limit:
                    place = ele['url']
                    #print(place)
                    hr_rank.append(place.split('/')[-1][:-18])
                i = i + 1
                #print(hr_rank)

            p = p + 1

        self.run_list(hr_rank, tags = tags)
    
    def run_author(self, locate, tags = []):
        '''not tested
            can found most of the pic of same author
            now can only use pic find pic, can not use author number
            and some pic info may be missed...'''
        url = self.trans_number(locate)
        req_init = requests.get(url)
        soup_init = bs(req_init.text,"html.parser")
        sel_one = soup_init.select("meta#meta-preload-data")
        sel_two = sel_one[0]["content"].split(',')

        hr_auth = []
        for sel in sel_two:
            try:
                hr_num = int(sel.split('"')[1])
                hr_auth.append(hr_num)
            except:
                pass
        
        self.run_list(hr_auth, tags = tags)
        
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

        
if __name__ == '__main__':
    #print(os.path.abspath('.'))
    #input()
    p = Pixiv()
    #p.get_mode()
    #p.get_pic(83113557, ["魔法少女まどか☆マギカ","星空ドレス"])
    #p.get_pic(82928832)
    #print(p.db.data)
    p.run_rank(date = 20200725, limit = 3)
    #p.run_author(11491793)
    #print(p.info)
    #for pic in p.info:
    #    p.info[pic].get_info()

            

        

