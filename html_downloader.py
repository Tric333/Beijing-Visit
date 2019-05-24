# coding=utf-8
__author__ = 'zyx'
import requests

class HtmlDownloader(object):
    #函数编解码方式应该从web页面获取
    def download(self, url,decoding='gbk',encoding='utf-8'):
        if url is None:
            return None
        html=requests.get(url,timeout=10)
        html=html.content.decode(decoding)
        return html
