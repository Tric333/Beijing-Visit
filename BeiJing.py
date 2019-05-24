import html_downloader,html_parser#,url_manager,html_outputer
import re

class SpiderMain(object):
    def __init__(self):
        #self.urls=url_manager.UrlManager()#管理URL
        self.downloader=html_downloader.HtmlDownloader()#下载URL内容
        self.parser=html_parser.HtmlParser()#解析URL内容
        #self.outputer=html_outputer.HtmlOutputer()#输出获取到的内容

def analyseDoc():
    f = open('data.txt','r',encoding='utf-8')
    d = open('pre_data.txt', 'w+',encoding='utf-8')
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

if __name__ == '__main__':
    data = analyseDoc()
    obj_spider = SpiderMain()
    dir = open('source.txt','w+',encoding='utf-8')
    error_dir = open('error_source.txt','w+',encoding='utf-8')
    max_repeat = 10
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
                print('repeat {}'.format(repeat))
                print(html_cont)
                print(i)
            if repeat == max_repeat:
                print('error_source record')
                error_dir.write(str(i)+'\n')
    dir.close()
    error_dir.close()
