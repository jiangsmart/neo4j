# author: Xilun Jiang
import sys
from conversation import Graph4Match
from userInfo import UserInfo

sys.path.append('/mnt/omada/router/code')
import twserver
from twserver import main


def start(usr_input):
    id = usr_input.split('$')[0]
    q = usr_input.split('$')[1]

    userinfo = UserInfo()
    g = Graph4Match(userinfo.ip, userinfo.user, userinfo.password)
    out = g.match_in_string(q)

    output = id + '$' + '3' + '#' + out + '*the_end'
    return output


if __name__ == '__main__':
    main(start, 10012, '0.0.0.0')
