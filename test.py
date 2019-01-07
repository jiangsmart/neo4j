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
            print n.find_route_for_num(graph)
        except:
            print '\n!!!!!!!!!!!\n!!!error!!!\n!!!!!!!!!!!\n' + str(i)


content = '泰国3333新加坡印度尼西亚'
result = re.search('(泰国|新加坡)(\d*)'.decode('utf8'), content.decode('utf8'))
# content = re.sub('我想', 'hahahahaah',content)
print result.group(0)
print result.group(1)
print result.group(2)
