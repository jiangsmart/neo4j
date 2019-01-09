# coding=utf-8
import re


class st():
    """
    现在没有加分词，后期出现问题用分词+正则解决
    """
    # poi_list = list()
    hanzinum = {u'一': u'1', u'二': u'2', u'三': u'3', u'四': u'4', u'五': u'5', u'六': u'6', u'七': u'7', u'八': u'8',
                u'九': u'9', u'零': u'0'}
    jijie = {u'冬天': u'12月', u'冬日': u'12月', u'冬季': u'12月', u'寒假': u'12月', u'夏天': u'8月', u'夏日': u'8月', u'夏季': u'8月',
             u'暑期': u'8月', u'暑假': u'8月'}

    def __init__(self, path='./poi_name.dat'):
        self.poi_list = list()
        self.nick_name = dict()
        in_file = open(path, 'r')
        for line in in_file:
            fields = line.strip().split()
            poi_name = fields[0]
            nick_names = [a for a in fields[1:]]
            self.poi_list.append(poi_name)
            self.poi_string = '|'.join(self.poi_list)
            if nick_names:
                self.nick_name[poi_name] = '|'.join(nick_names)

    def standardlize(self, content):
        content = content

        # 去除标点符号
        content = re.sub("[\s+\.\!\/_,$%^*():+\"\']+|[+——！，。？?、~@#￥%……&*（）：；【】〔〕“”《》]+",
                         u"", content)

        # 数字标准化
        for (hanzi, num) in self.hanzinum.items():
            content = re.sub(u'%s[天日]' % hanzi, u"%s天" % num, content)

        # 季节标准化 冬天冬日冬季寒假-12月 夏天夏日夏季暑期暑假-8月
        for (nick, serious) in self.jijie.items():
            content = re.sub(nick, serious, content)

        # 地名标准化
        for (poi_name, nick_string) in self.nick_name.items():
            content = re.sub(nick_string, poi_name, content)

        # 去除首尾空格
        content = content.strip()

        # content = content.encode('utf8')

        print('finish standard')
        return content


if __name__ == '__main__':
    s = st()
    # print s.standardlize('玩七天')
    print(s.standardlize('我想暑假去凤凰机场玩五天'))
    print(s.poi_list)
    # print st.poi_list
