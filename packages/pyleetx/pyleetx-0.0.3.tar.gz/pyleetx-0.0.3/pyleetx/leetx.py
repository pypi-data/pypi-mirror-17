#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re


class BASE(object):
    url = 'http://1337x.to'
    search = '/search/{}/1/'


class Torrent(object):
    def __init__(self, title, magnet, size, seeds, leeches):
        self.title = title
        self.magnet = magnet
        self.size = size
        self.seeds = seeds
        self.leeches = leeches


def search(query):
    headers = {'User-Agent' : "Magic Browser"}
    req_url = BASE.url + BASE.search.format(quote_plus(query))
    s = requests.get(req_url, headers=headers, verify=False)
    html = s.content
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', {'class': 'clearfix'})
    try:
        li = ul.find_all('li')
    except AttributeError as e:
        return []

    torrents = []
    for item in li:
        str_link = str(item.strong.a)
        m = re.search('"(.*?)"', str_link)
        link = m.group().strip('\"')
        title = link.split('/')[-2]
        title = re.sub('-', ' ', title)

        div = item.find_all('div')

        size = div[3].text
        seeds = int(re.sub(',', '', div[1].text))
        leeches = int(re.sub(',', '', div[2].text))

        req_url = BASE.url + link
        s = requests.get(req_url, headers=headers, verify=False)
        html = s.content
        soup = BeautifulSoup(html, 'html.parser')
        down_ul = soup.find('ul', {'class': 'download-links btn-wrap-sm'})
        mag = down_ul.li.a.get('href')

        torrents.append(Torrent(title, mag, size, seeds, leeches))

    return torrents
