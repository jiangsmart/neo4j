# coding=utf-8

import neo4j_drive as n
import re
import tools
from py2neo import Graph
from userInfo import UserInfo

"""
目前问题：
三亚凤凰机场附近等POI附近包含三亚等目的地名称,目前因为先识别POI所以没有问题,以后需要注意修正
"""


def match_in_string(in_string):
    userinfo = UserInfo()
    graph = Graph(userinfo.ip, username=userinfo.user, password=userinfo.password)
    not_found_string = '对不起，没有符合您条件的信息'
    not_understood_string = '对不起，我不懂您的意思'
    out_dur_range_string = '对不起，游览天数一般在3~8天'
    s = tools.st()

    # 预处理
    in_string = s.standardlize(in_string)

    # 按标号查询路线
    reObject1 = re.search(r'第(\d*)[条号]'.decode('utf8'), in_string.decode('utf8'))
    if reObject1:
        out = n.find_route_for_num(graph, reObject1.group(1))
        if out == '':
            out = not_found_string
        return out
    print 'finish 1'

    # 查询热门景点
    reObject2 = re.search(r'(热门|欢迎|经典).*景'.decode('utf8'), in_string.decode('utf8'))
    if reObject2:
        out = n.find_top_scenic_spot(graph)
        if out == '':
            out = not_found_string
        return out
    print 'finish 2'

    # 查询特定天去特定景点
    reObject3 = re.search(u'第(\d*)天(游览|去|参观|游玩|观赏|玩)(%s)' % s.poi_string, in_string.decode('utf8'))
    if reObject3:
        # out = n.find_route_for_scenic_day(graph, '三亚凤凰机场附近', 2)
        out = n.find_route_for_scenic_day(graph, reObject3.group(3), reObject3.group(1))
        if out == '':
            out = not_found_string
        return out
    print 'finish 3'

    # 上述不匹配，按照(季节,游览时间,目的地)匹配
    dur = re.search(u'[^第](\d*)天', in_string.decode('utf8'))
    des = re.search(u'(三亚|海口)', in_string.decode('utf8'))
    season = re.search(u'(8月|12月)', in_string.decode('utf8'))
    if dur or des or season:
        if not dur:
            dur_in = '*'
        elif 3 <= int(dur.group(1)) <= 8:
            dur_in = dur.group(1)
        else:
            return out_dur_range_string

        if not des:
            des_in = '*'
        elif des.group() == u'海口':
            des_in = 'haikou'
        elif des.group() == u'三亚':
            des_in = 'sanya'
        else:
            raise ValueError('des.group():%s' % des.group())

        if not season:
            season_in = '*'
        elif season.group() == u'8月':
            season_in = 'summer'
        elif season.group() == u'12月':
            season_in = 'winter'
        else:
            raise ValueError('season.group():%s' % season.group())
        print dur_in + des_in + season_in
        out = n.find_route_for_des_season_dur(graph, des_in, season_in, dur_in)
        # if out == '':
        #     out = '对不起，您查询的不存在'
        # out = dur.group(1) + des.group() + season.group()
        return out
    print 'finish 4'
    return not_understood_string


if __name__ == '__main__':
    # in_string = '查询第10条旅游线路'
    # in_string = '最受欢迎的景区是什么？'
    in_string = '我想去三亚玩5天'
    out = match_in_string(in_string)
    print out
