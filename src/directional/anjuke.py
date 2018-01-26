#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

'''
    安居客 面积小于50的房屋
'''
url="https://xa.fang.anjuke.com/fangyuan/"

def down_load(url):
    html = requests.get(url).content
    return html

def find_house(html):
    soup = BeautifulSoup(html, 'lxml')
    house_list = soup.find('div', attrs={'class': 'F-list'})
    for house_item in house_list.find_all('div', attrs={'class': 'item-mod'}):
         house_image_url = house_item.find('div', attrs={'class': 'F-pic'}).find('img').get('src')

         house_dl = house_item.find('dl', attrs={'class': 'F-info'})
         house_dl_dd = house_dl.find_all('dd')
         em2Text = house_dl_dd[0].find_all('em')[1].getText()
         em3Text = house_dl_dd[0].find_all('em')[2].getText()
         house_arre = house_dl_dd[1].find_all('a')[0].getText()
         house_name = house_dl_dd[1].find_all('a')[2].getText()
         if(float(em2Text[0:-2])<=50):
            print('户型图：', house_image_url, '面积：', em2Text, em3Text, '名称：', house_arre, house_name)

    house_page = soup.find('div', attrs={'class': 'pagination'})
    house_page_next = house_page.find('a', attrs={'class': 'next-page next-link'})
    if house_page_next:
        return url+house_page_next.get('href')
    return None



def main():
    Url = url
    while Url:
        Url = find_house(down_load(Url))

if __name__ == "__main__":
    main()
