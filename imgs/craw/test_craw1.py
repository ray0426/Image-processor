import requests
from bs4 import BeautifulSoup
# import json
def test_1():
    p = requests.Session()
    headers = {
        'Referer': 'https://www.google.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }
    url = p.get("https://www.pixiv.net/ranking.php", data = headers)
    soup = BeautifulSoup(url.text,"html.parser")
    print(soup.prettify())

if __name__ == "__main__":
    test_1()