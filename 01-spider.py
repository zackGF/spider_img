import json
from urllib.parse import urlencode
from multiprocessing import Pool
from selenium import webdriver
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from hashlib import md5

def main(pagenum):
    text = get_one_page(pagenum, '美女')
    # print(text)
    for item in parse_one_page(text):
        if item:
            # print(item)
            get_url_detail(item)


browser = webdriver.Chrome()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
}


def get_one_page(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)
    try:
        response = requests.get(url, headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('获取失败')
        return None


def parse_one_page(text):
    data = json.loads(text)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_url_detail(url):
    browser.get(url)
    detail_text = browser.page_source
    soup = BeautifulSoup(detail_text, 'lxml')
    img_type_1 = soup.select('div.pgc-img>img')
    img_type_2 = soup.select('div.image-item-inner>img')
    if img_type_1:
        for img in img_type_1:
            tp1src = img.get('src')
            print(tp1src)
            name = md5(tp1src.encode()).hexdigest()
            resp = requests.get(tp1src)
            with open('D:/code/爬虫/day05/project/img/' + name + '.jpg', 'wb') as f:
                f.write(resp.content)
                f.close()
    elif img_type_2:
        for img in img_type_2:
            tp2src = img.get('data-src')
            print(tp2src)
            name = md5(tp2src.encode()).hexdigest()
            resp = requests.get(tp2src)
            with open('D:/code/爬虫/day05/project/img/' + name + '.jpg', 'wb') as f:
                f.write(resp.content)
                f.close()
    else:
        print("None")


if __name__ == '__main__':
    # for num in range(5):
    #     main(num * 20)
    pool = Pool()
    pool.map(main, [num * 20 for num in range(5)])
