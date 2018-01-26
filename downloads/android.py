#coding:utf8
import requests,time,MySQLdb, setting, get_proxy_mysql,re,download
config = setting.configs
url_db = config['url_db']
host = url_db['host']
user = url_db['user']
password = url_db['password']
db_name = url_db['database']
local_path = setting.save_path()
def android(data):
    url = data[1]
    print url
    proxy = get_proxy_mysql.get_proxy()
    if proxy:
        text = requests.get(url,proxies=proxy).text
    else:
        text = requests.get(url).text
    re_url = re.compile(r'<div id=download></div><a href=(.*?)><input')
    url = re.search(re_url,text)
    re_type = re.compile(r'<div class="title">(.*?)</div>')
    file_type = re.search(re_type,text)
    if url:
        if file_type:
            url = url.group(1)
            file_type = file_type.group(1).strip()[-4:]
            id = data[0]
            file_name = local_path + data[2] + file_type
            print file_name
            download.download(url,file_name,id)
    else:
        print 'android网站,未匹配到下载的URL'