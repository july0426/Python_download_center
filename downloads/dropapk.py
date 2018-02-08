#coding:utf8
import requests,time,MySQLdb, setting, get_proxy_mysql,re,download
config = setting.configs
url_db = config['url_db']
host = url_db['host']
user = url_db['user']
password = url_db['password']
db_name = url_db['database']
local_path = setting.save_path()
def dropapk(data):
    url = data[1]
    print url
    datas = {
        'op': 'download2',
        'id': url.split('/')[-1],
        'rand': '',
        'referer': url,
        'method_free': 'Free Download',
        'method_premium': '',
        'adblock_detected': '0',
    }
    proxy = get_proxy_mysql.get_proxy()
    if proxy:
        text = requests.post(url,data = datas,proxies=proxy).text
    else:
        text = requests.post(url,data = datas).text
    re_url = re.compile(r'<a href="(.*?)"><img src="https://dropapk.com/images_mega/down_final.png"')
    url = re.search(re_url,text)
    if url:
        url = url.group(1)
        print url
        file_type = url[-4:]
        id = data[0]
        file_name = local_path + data[2] + file_type
        print file_name
        download.download(url,file_name,id)
    else:
        print 'dropapk.com网站的下载链接没有匹配到'