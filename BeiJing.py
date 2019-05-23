import re


def analyseDoc():
    f = open('data.txt','r',encoding='utf-8')
    d = open('pre_data.txt', 'w+',encoding='utf-8')
    node = {}
    for i in f.readlines():
        data_name = re.search('data-name=".*" data-top',i).group().replace('data-name=','').replace(' data-top','').replace('\"','')
        html = re.search('\"https://.*\.html"',i).group().replace('\"','')
        comment_score = re.search('score">.{1,6}分',i).group().\
                        replace('score">','').replace('分','')
        comment_count = re.search('>.{1,6}条点评',i).group().\
                        replace('>','').replace('条点评','')
        landmark_outbox = re.search('距市中心.{1,6}m',i).group().\
                        replace('距市中心','')

        sub_node = {'data_name':data_name,
                    'html':html,
                    'comment_score':comment_score,
                    'comment_count':comment_count,
                    'landmark_outbox':landmark_outbox}
        d.write(str(sub_node)+'\n')
        node[data_name] = sub_node
        # print(data_name)
        # print(html)
        # print(comment_score)
        # print(comment_count)
        # print(landmark_outbox)
    print(node)
    f.close()
    d.close()

if __name__ == '__main__':
    analyseDoc()