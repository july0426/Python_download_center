#coding:utf8
import random,os,stat
configs = {
    'url_db': {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'test'
    },
    'proxy_db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'www-data',
        'password': 'www-data',
        'database': 'awesome'
    },
    'local_path':'/users/qiyue/myxuni/pngtree/download_python/'
}
def save_path():
    dir_array = ("q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v","b")
    savepath = configs['local_path'] + random.choice(dir_array) + "/" + random.choice(dir_array) + "/" + random.choice(dir_array) + "/"
    if os.path.exists(savepath):
        pass
    else:
        os.makedirs(savepath)
        os.chmod(savepath, stat.S_IRWXG | stat.S_IRWXU | stat.S_IRWXO)
    # print savepath
    return savepath