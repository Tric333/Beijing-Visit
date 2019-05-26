import html_downloader,html_parser#,url_manager,html_outputer
import re
# import numpy as np
# import pandas as pd

class SpiderMain(object):
    def __init__(self):
        #self.urls=url_manager.UrlManager()#管理URL
        self.downloader=html_downloader.HtmlDownloader()#下载URL内容
        self.parser=html_parser.HtmlParser()#解析URL内容
        #self.outputer=html_outputer.HtmlOutputer()#输出获取到的内容

def analyseDoc():
    f = open('web_data.txt','r',encoding='utf-8')
    d = open('data.txt', 'w+',encoding='utf-8')
    node = []
    for i in f.readlines():
        try:
            data_name = re.search('data-name=".*" data-top',i).group().replace('data-name=','').replace(' data-top','').replace('\"','')
            html = re.search('\"https://.*\.html"',i).group().replace('\"','')
            comment_score = re.search('score">.{1,6}分',i).group().\
                            replace('score">','').replace('分','')
            comment_count = re.search('>.{1,6}条点评',i).group().\
                            replace('>','').replace('条点评','')
            landmark_outbox = re.search('距市中心.{1,6}m',i).group().\
                            replace('距市中心','')
            if re.search('</i>.{1,5}<span>起',i) != None:
                price = re.search('</i>.{1,5}<span>起',i).group().\
                        replace('</i>','').replace('<span>','').replace('起','')
            else:
                price = 0
        except :
            print(i)

        sub_node = {'name':data_name,
                    'html':html,
                    'comment_score':comment_score,
                    'comment_count':comment_count,
                    'landmark_outbox':landmark_outbox,
                    'price':price}
        d.write(str(sub_node)+'\n')
        node.append(sub_node)
    f.close()
    d.close()
    return node

def parse_place(soup):
    nodes = soup.find('div', class_="opening_hours js_web")
    ret = {}
    if nodes is not None:
        for node in nodes:
            try:  # 开业时间
                ret['opentime'] = nodes.find('span').string
            except:
                ret['opentime'] = None
            try:  # 游玩时间
                ret['time'] = nodes.find('div', style="width: 100%;padding-left: 28px;font-size: 12px;text-overflow: ellipsis;white-space: nowrap;overflow: hidden").string
            except:
                ret['time'] = None
    return ret

def getsourcedata():
    data = analyseDoc()
    obj_spider = SpiderMain()
    dir = open('source.txt','w+',encoding='utf-8')
    max_repeat = 4
    for i in data:
        repeat = 0
        while repeat < max_repeat:
            try:
                html_cont = obj_spider.downloader.download(i['html'],'utf-8','utf-8')
                ans = obj_spider.parser.parse(html_cont, encoding='utf-8', parse_fun=parse_place)
                i['opentime'], i['time']  = ans['opentime'], ans['time']
                print(i)
                dir.write(str(i)+'\n')
                break
            except :
                repeat+=1
                print('repeat {} \n{}\n{}'.format(repeat,html_cont,i))
            if repeat == max_repeat:#超过max_repeat获取失败认为没有读取到关键字，写入None
                i['opentime'], i['time']  = None, None
                dir.write(str(i)+'\n')
    dir.close()
def landmark_outbox_pre(data):
    for i in data:
        dis = i['landmark_outbox']
        if 'km' in dis:
            i['landmark_outbox'] = float(dis.replace('km',''))
        elif 'm' in dis:
            i['landmark_outbox'] = float(dis.replace('m',''))/1000
        else:
            print(dis)
def time_pre(data):
    for i in data:
        time_raw = i['time']
        if '天' in time_raw:
            a = time_raw.replace('天','').split('-')
            temp = 0
            for _ in a:
                temp += float(_)*8*60
            i['time'] = temp/len(a)
        elif '小时' in time_raw:
            a = time_raw.replace('小时','').split('-')
            temp = 0
            for _ in a:
                temp+=float(_)*60
            i['time'] = int(temp/len(a))
        elif '分钟' in time_raw:
            a = time_raw.replace('分钟','').split('-')
            temp = 0
            for _ in a:
                temp+=float(_)
            i['time'] = int(temp/len(a))
        elif time_raw == '0':
            i['time'] = 0

def comment_count_pre(data):
    for i in data:
        if '万' in i['comment_count']:
            i['comment_count'] = int(float(i['comment_count'].replace('万',''))*10000)
        else:
            i['comment_count'] = int(i['comment_count'])
    return

def comment_score_pre(data):
    for i in data:
        i['comment_score'] = float(i['comment_score'])
    return

def preprocessdata(data):
    landmark_outbox_pre(data)
    time_pre(data)
    comment_count_pre(data)
    comment_score_pre(data)
    return

def filterdata(data):
    res = []
    for i in data:
        if i['comment_score'] < 4.5 or \
            i['comment_count'] < 100 or \
            i['landmark_outbox'] >200 or \
            i['time'] == 0:
            continue
        res.append(i)
        print(i)
    return res

if __name__ == '__main__':
    f = open('source.txt','r',encoding='utf-8')
    data = []
    for i in f.readlines():
        data.append(eval(i))
    preprocessdata(data)
    ret = filterdata(data)
    d = open('pre_date.txt','w+',encoding='utf-8')
    for i in ret:
        d.write(str(i)+'\n')
    d.close()