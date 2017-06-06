#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author  : mundane
# @time    : 2017/6/6 10:08
# @file    : SearchFavorite.py
# @Software: PyCharm Community Edition

import requests, re, json
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'Cookie': '',  # 你的cookie
    'Host': 'www.jianshu.com',
    'Connection': 'keep-alive'
}
datas = []


def download_html(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print('response.status_code =', response.status_code)
        return None
    return response.text


if __name__ == '__main__':
    root_url = 'http://www.jianshu.com/bookmarks'
    html_content = download_html(root_url)
    soup = BeautifulSoup(html_content, 'lxml')
    print('正在解析, 请稍后...')
    text = soup.find(text=re.compile('page.+totalPages'))
    totalPages = json.loads(text).get('totalPages')
    for i in range(1, totalPages + 1):
        page_url = 'http://www.jianshu.com/bookmarks?page=%d' % i
        page_html_content = download_html(page_url)
        page_soup = BeautifulSoup(page_html_content, 'lxml')
        a_list = page_soup.find_all('a', class_='title', target='_blank', href=re.compile(r'/p/.+'))
        for a in a_list:
            url = 'http://www.jianshu.com' + a['href']
            title = a.text
            item = {'title': title, 'url': url}
            datas.append(item)

    fout = open('output.html', 'w', encoding='utf-8')
    fout.write('<html><head><meta charset="UTF-8"></head>')
    fout.write('<html>')
    fout.write('<body>')
    for data in datas:
        fout.write('<a class="title" href="%s">%s</a>' % (data['url'], data['title']))
        fout.write('<br />')
    fout.write('</body>')
    fout.write('</html>')

    keyword = input('请输入要搜索的关键字: ')
    for data in datas:
        m = re.search(keyword, data['title'], re.IGNORECASE)
        if m:
            print(data)