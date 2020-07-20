import urllib
import http.cookiejar
from bs4 import BeautifulSoup

class Pixiv:
    def __init__(self):
# 請求報文需要的一些資訊
# 登陸地址
        self.loginURL = 'https://www.pixiv.net/login.php'
# 頭部資訊
        self.loginHeader = {
            'Host': "www.pixiv.net",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/"  
            "537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
            'Referer': "http://www.pixiv.net/",
            'Content-Type': "application/x-www-form-urlencoded",
            'Connection': "keep-alive"
        }
# 包括使用者名稱、密碼等表單資訊
        self.postData = urllib.parse.urlencode({
            'mode': 'login',
            'return_to': '/',
            'pixiv_id': '',
            'pass': '',
            'skip': '1'}).encode("utf-8")
# cookie資訊，伺服器用來識別使用者身份
# 獲取本地cookie資訊，構建一個包含cookie資訊的opener
        self.cookie = http.cookiejar.LWPCookieJar()
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.cookieHandler)

    def get_first_page(self):
# 向伺服器發起請求，請求報文內容包括：URL，頭部，表單；請求方式為post
        request = urllib.request.Request(self.loginURL, self.postData, self.loginHeader)
        response = urllib.request.urlopen(request).decode("utf-8")
        print(response)
#        html = response.read().decode('utf-8')
#        print(html)
        #self.soup = BeautifulSoup(request,"html.parser")
        #print(self.soup.prettify())
# 用我們新建的包含cookie資訊的opener開啟，並返回伺服器響應報文
        #response = self.opener.open(request)
# 內容讀取，並以UTF-8解碼
        #content = response.read().decode('utf-8')
        #return content

if __name__ == "__main__":
    p=Pixiv()
    p.get_first_page()
