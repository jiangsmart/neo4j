# coding=utf-8
import json

in_file = open('/home/jiang/youyou6/routeInfo.json', 'r')
id_count = 0
out_file = open('/home/jiang/youyou6/routeInfo_route2.json', 'w')
for in_content in in_file:
    route = dict()
    json_content = json.loads(in_content)
    days_traj = json_content['trajectory']
    route['id'] = id_count
    route['des'] = json_content['des']
    route['season'] = json_content['season']
    days = json_content['days']
    route['dur'] = days
    route['type'] = json_content['type']
    traj = list()
    pois_lastday = None
    last_name = None
    for day_of_trip, day_traj in enumerate(days_traj):
        # if day_of_trip == days - 1:
        #     # 行程的最后一天处理ending_poi的问题
        #     pois_lastday = len(day_traj)
        for poi_of_day, poi in enumerate(day_traj):
            if poi_of_day == 0 and day_of_trip == 0:
                last_name = poi['name'].encode('utf-8')
                continue
                # if pois_lastday:
                # 非最后一天的处理
            visit = dict()
            visit['name1'] = last_name
            visit['name2'] = poi['name'].encode('utf-8')
            visit['day'] = day_of_trip + 1
            visit['activity'] = poi_of_day
            traj.append(visit)
            route['traj'] = traj
            last_name = visit['name2']
    json.dump(route, out_file, ensure_ascii=False, sort_keys=True)
    out_file.write('\n')
    # route[id_count]['traj'] = traj
    id_count += 1
# json.dump(route, out_file, ensure_ascii=False, indent=1, sort_keys=True)
