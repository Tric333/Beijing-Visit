#coding=utf8
__author__ = 'zyx'
from bs4 import BeautifulSoup

class HtmlParser(object):
    def parse(self,html_cont,encoding='gb2312',parse_fun = ''):
        if html_cont is None or parse_fun == '':
            return
        else:
            soup=BeautifulSoup(html_cont,'html.parser',from_encoding=encoding)
            return parse_fun(soup)
