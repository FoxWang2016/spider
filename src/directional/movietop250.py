#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

'''
    豆瓣 电影Top250 抓取
'''

Url = "http://movie.douban.com/top250/"

def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data

def main():
    href = Url
    while(href):
        href = find_movie_name(download_page(href))

def find_movie_name(html):
    soup = BeautifulSoup(html, 'lxml')
    movie_ol = soup.find('ol', attrs={'class': 'grid_view'})
    for movie_li in movie_ol.find_all('li'):
        movie_li_hd = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = movie_li_hd.find('span', attrs={'class': 'title'}).getText()
        movie_url = movie_li_hd.find('a').get('href')
        movie_pic = movie_li.find('div', attrs={'class': 'pic'})
        i = movie_pic.find('em').getText()
        print(i, 'movie_name:', movie_name, 'movie_url:', movie_url)

    movie_paginator = soup.find('div', attrs={'class': 'paginator'})
    movie_paginator_next = movie_paginator.find('span', attrs={'class': 'next'})
    movie_paginator_next_a = movie_paginator_next.find('a')
    if movie_paginator_next_a:
        next_href = movie_paginator_next_a.get('href')
        return Url + next_href
    return None

if __name__ == '__main__':
    main()
