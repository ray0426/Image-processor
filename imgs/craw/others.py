import urllib
import http.cookiejar

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
        self.postData = urllib.urlencode({
            'mode': 'login',
            'return_to': '/',
            'pixiv_id': '1983475717@qq.com',
            'pass': '********',
            'skip': '1'})
# cookie資訊，伺服器用來識別使用者身份
# 獲取本地cookie資訊，構建一個包含cookie資訊的opener
        self.cookie = http.cookiejar.LWPCookieJar()
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.cookieHandler)