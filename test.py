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


content = '我想第3天玩大东海'
# content = '泰国3333新加坡印度尼西亚'
                     #1  #2    #    #3                     #4
result1 = re.search('(第)(\d*)[日天](游览|去|参观|游玩|观赏|玩)(大东海)', content)
                     #    #1    #     #2
result2 = re.search('[^第](\d*)[日天].*(大东海)', content)

# result3 = re.search('[^第](\d*)(天|日)')
# content = re.sub('我想', 'hahahahaah',content)
if result1:
    print('1.0\t'+result1.group(0))
    print('1.1\t'+result1.group(1))
    print('1.2\t'+result1.group(2))
    print('1.3\t'+result1.group(3))
    print('1.4\t'+result1.group(4))

if result2:
    print('2.0\t'+result2.group(0))
    print('2.1\t'+result2.group(1))
    print('2.2\t'+result2.group(2))

