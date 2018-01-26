#coding:utf8
import requests,time,MySQLdb, setting, get_proxy_mysql,re,download
config = setting.configs
url_db = config['url_db']
host = url_db['host']
user = url_db['user']
password = url_db['password']
db_name = url_db['database']
local_path = setting.save_path()
def zippyshare(data):
    url = data[1]
    print url
    proxy = 0
    # proxy = get_proxy_mysql.get_proxy()
    if proxy:
        res = requests.get(url,proxies=proxy)
    else:
        res = requests.get(url)
    text = res.text
    re_url = re.compile(r'document\.getElementById\(\'dlbutton\'\)\.href = (.*?);')
    url_data = re.search(re_url,text)
    if url_data:
        url_data = url_data.group(1)
        print url_data
        re_num = re.compile(r'\((.*?)\)')
        num = re.search(re_num, url_data)
        num = num.group(1)
        print num
        nu = eval(num)
        print nu
        url_data = url_data.split('"')
        print url_data
        url = 'http://www101.zippyshare.com' + url_data[1] + str(nu) + url_data[-2]
        print url
        file_type = url[-4:]
        id = data[0]
        file_name = local_path + data[2] + file_type
        print file_name
        download.download(url,file_name,id)