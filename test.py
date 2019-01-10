# coding=utf-8
import neo4j_drive as n
import re
from py2neo import Graph
from userInfo import UserInfo


def out_test():
    userinfo = UserInfo()
    graph = Graph(userinfo.ip, username=userinfo.user, password=userinfo.password)
    for i in range(0, 76):
        try:
            print(n.find_route_for_num(graph))
        except:
            print('\n!!!!!!!!!!!\n!!!error!!!\n!!!!!!!!!!!\n' + str(i))


content = '我想去三亚第2天'
# content = '泰国3333新加坡印度尼西亚'
result = re.search('[^第](\d*)天', content)
# content = re.sub('我想', 'hahahahaah',content)
print(result.group(0))
print(result.group(1))
print(result.group(2))
