import requests
from bs4 import BeautifulSoup as bs
import time
# import json
pixiv_id = ""
password = ""

def test_1():
#    p = requests.Session()

    headers = {
        'Referer': 'https://www.google.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    postData = {
            'mode': 'login',
            'return_to': '/',
            'pixiv_id': '',
            'pass': '',
            'skip': '1'
    }
#    url = p.get("https://www.pixiv.net/ranking.php", headers = headers, data = postData)
#    soup = BeautifulSoup(url.text,"html.parser")
#    print(soup.prettify())

def test_2():
    
    r = requests.Session()

    payload = {
        'pixiv_id':pixiv_id ,
        'password':password
    }

    r.post("https://www.pixiv.net/login.php", data = payload)
    r_2= r.get("https://www.pixiv.net")

    print(r_2.text)

def test_3():
    payload = {
        'pixiv_id':pixiv_id ,
        'password':password
    }
    headers={
        "Host": "www.pixiv.net" , 
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }
    res=requests.post("https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh_tw&source=pc&view_type=page",data=payload,)
    print(res.text)

def test_craw_rank_easy():
    path = "./imgs/craw/pic/test/"
    url = "https://www.pixiv.net"
    head = {
        "user-agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    } 

    req_rank = requests.get("https://www.pixiv.net/ranking.php")
    soup_rank = bs(req_rank.text,"html.parser")
    sel_rank = soup_rank.select("div.ranking-image-item a")

    hr_rank = []
    for s in sel_rank:
        hr_rank.append(s["href"])

    for hr in hr_rank:
        title = hr[-8:]
        req_page = requests.get(url+hr)
        head["referer"] = url + hr
        soup_page = bs(req_page.text,"html.parser")
        sel_page = soup_page.select("meta#meta-preload-data")

        try:
            for part in sel_page[0]["content"].split(','):
                if "regular" in part:
                    req_pic = requests.get(part[11:-1] , headers = head)
                    img = req_pic.content
                    filename = title+'.png'
                    with open (path + filename , 'wb') as pic:
                        pic.write(img)  #prob
                    break
        except:
            print(soup_page.select("meta"))
            return
        
        time.sleep(1)



if __name__ == "__main__":
    #with open ('./craw')
    test_craw_rank_easy()
