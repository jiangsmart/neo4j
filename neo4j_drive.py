# coding=utf-8
"""
目前问题：格式不统一,r.dur数字是字符串类型,r.day,r.activity是数字类型
"""
from py2neo import Graph, Node, Relationship  # NodeSelector
from userInfo import UserInfo


def get_route_string(results):
    out = ''
    last_route_day = 3
    # get results
    for result in results:
        begin_node = result['a.name'].encode('utf-8')
        end_node = result['b.name'].encode('utf-8')
        route_day, route_activity, route_id = result['r.day'], result['r.activity'], result['r.tripline_id']
        if route_day < last_route_day:  # and route_activity == 1:
            if route_day == 1:
                out += '\nroute%s:\nday1:%s-->%s' % (str(route_id), begin_node, end_node)
            elif route_day == 2:
                out += '\nroute%s:\nday1:%s\nday2:%s' % (str(route_id), begin_node, end_node)
            else:
                print 'error:begin_route_day>2!!!!'
        elif route_day > last_route_day:
            out += '\nday%s:%s' % (str(route_day), end_node)
        else:
            out += '-->%s' % end_node
        last_route_day = route_day
    return out.strip()


def get_poi_string(results):
    out = ''
    for result in results:
        out += (result['poi1']['name'] + '\n')
    return out


# 目的地为某地，季节为某季节，持续时间为几天
def find_route_for_des_season_dur(graph, des, season, dur):
    pattern = "MATCH (a)-[r:Route]->(b) " \
              "WHERE r.des=%s AND r.season=%s AND r.dur=%s " \
              "RETURN a.name,b.name,r.day,r.activity,r.tripline_id " \
              "ORDER BY r.tripline_id,r.day,r.activity"

    if des == '*':
        des_in = "~'.*'"
    else:
        des_in = "'" + des + "'"

    if dur == '*':
        dur_in = "~'.*'"
    else:
        dur_in = "'" + dur + "'"

    if season == '*':
        season_in = "~'.*'"
    elif season == 'summer':
        season_in = "'201508'"
    elif season == 'winter':
        season_in = "'201512'"
    else:
        raise ValueError('season input error: %s' % season)

    cypher = pattern % (des_in, season_in, dur_in)
    results = graph.run(cypher).data()
    out = get_route_string(results)
    return out


# 经过某景区的路线
def find_route_for_scenic(graph, scenic):
    pattern = "MATCH (n)-[r1:Route]->(m) " \
              "WHERE m.name='%s' OR n.name='%s' " \
              "WITH DISTINCT r1.tripline_id AS rid " \
              "MATCH p = (a) - [r:Route{tripline_id: rid}]->(b) " \
              "RETURN a.name,b.name,r.day,r.activity,r.tripline_id " \
              "ORDER BY r.tripline_id,r.day,r.activity"
    cypher = pattern % (scenic, scenic)
    results = graph.run(cypher).data()
    out = get_route_string(results)
    return out


# 经过某景区且玩几天的路线
def find_route_for_scenic_dur(graph, scenic, dur):
    pattern = "MATCH (n)-[r1:Route]->(m) " \
              "WHERE r1.dur='%s' AND (m.name='%s' OR n.name='%s') " \
              "WITH DISTINCT r1.tripline_id AS rid " \
              "MATCH p = (a) - [r:Route{tripline_id: rid}]->(b) " \
              "RETURN a.name,b.name,r.day,r.activity,r.tripline_id " \
              "ORDER BY r.tripline_id,r.day,r.activity"
    dur = str(dur)
    cypher = pattern % (dur, scenic, scenic)
    results = graph.run(cypher).data()
    out = get_route_string(results)
    return out


# 第几天经过某景区的路线
def find_route_for_scenic_day(graph, scenic, day):
    pattern = "MATCH (n)-[r1:Route]->(m) " \
              "WHERE r1.day=%s AND (m.name='%s' OR n.name='%s') " \
              "WITH DISTINCT r1.tripline_id AS rid " \
              "MATCH p = (a) - [r:Route{tripline_id: rid}]->(b) " \
              "RETURN a.name,b.name,r.day,r.activity,r.tripline_id " \
              "ORDER BY r.tripline_id,r.day,r.activity"
    # p = (a) - [r2:Route{tripline_id: rid}]->(b)
    # (a:POI{name:'大东海'})-[:Route*]->(b)
    day = str(day)
    cypher = pattern % (day, scenic, scenic)
    results = graph.run(cypher).data()
    out = get_route_string(results)
    return out


# 最热门的景点
def find_top_scenic_spot(graph):
    cypher = 'MATCH (poi1)-[r:Route]-(poi2) ' \
             'WITH poi1, count(r) AS routes ' \
             'RETURN poi1' \
             ' ORDER BY routes DESC limit 3'
    results = graph.run(cypher).data()
    out = get_poi_string(results)
    return out


# 根据标号查询路线
def find_route_for_num(graph, num):
    pattern = "MATCH p=(a)-[r:Route{tripline_id:%s}]->(b) " \
              "RETURN a.name,b.name,r.tripline_id,r.day,r.activity " \
              "ORDER BY r.day,r.activity"
    cypher = pattern % num
    results = graph.run(cypher).data()
    out = get_route_string(results)
    return out


if __name__ == '__main__':
    userinfo = UserInfo()
    g = Graph(userinfo.ip, username=userinfo.user, password=userinfo.password)
    out_string = find_route_for_des_season_dur(g, 'sanya', 'summer', '*')
    # out_string = find_route_for_scenic_dur(g, '三亚凤凰机场附近', 8)
    # out_string = find_route_for_scenic_day(g, '三亚凤凰机场附近', 1)
    # out_string = find_route_for_scenic(g, '三亚凤凰机场附近')
    # out_string = find_top_scenic_spot(g)
    # out_string = find_route_for_num(g, 5)
    print out_string
