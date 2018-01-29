#-*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

'''
    豆瓣 按评分排序的图书Top250 抓取
'''

Url = "https://book.douban.com/top250"
book_list = []

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
    for book in sorted(book_list, key=lambda x: (x[2], x[3]), reverse=True):
        print(book)

def find_movie_name(html):
    soup = BeautifulSoup(html, 'lxml')
    book_div = soup.find('div', attrs={'class': 'indent'})
    #book_table = book_div.find_all('table')
    for book_table in book_div.find_all('table'):
        book_tr = book_table.find('tr', attrs={'class': 'item'})
        book_td = book_tr.find_all('td')
        book_name = book_td[1].find('div', attrs={'class': 'pl2'}).find('a').get('title')
        book_author = book_td[1].find('p', attrs={'class': 'pl'}).get_text()
        book_rating = book_td[1].find('div', attrs={'class': 'star clearfix'}).find('span', attrs={
                'class': 'rating_nums'}).get_text()
        book_pjr = re.findall("\d+", book_td[1].find('div', attrs={'class': 'star clearfix'}).find('span', attrs={
                'class': 'pl'}).get_text())
        #print(type(book_pjr))
        temp = (book_name, book_author, book_rating, book_pjr[0])
        book_list.append(temp)

    book_paginator = soup.find('div', attrs={'class': 'paginator'})
    book_paginator_next = book_paginator.find('span', attrs={'class': 'next'})
    book_paginator_next_a = book_paginator_next.find('a')
    if book_paginator_next_a:
        next_href = book_paginator_next_a.get('href')
        return next_href
    return None


if __name__ == '__main__':
    main()