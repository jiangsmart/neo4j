class UserInfo:
    def __init__(self, path='./userInfo.dat'):
        in_file = open(path, 'r')
        self.ip = in_file.readline().strip()
        self.user = in_file.readline().strip()
        self.password = in_file.readline().strip()


if __name__ == '__main__':
    userinfo = UserInfo()
    print userinfo.ip
    print userinfo.user
    print userinfo.password
