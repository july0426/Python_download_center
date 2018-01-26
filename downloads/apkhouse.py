#coding:utf8
import requests,time,MySQLdb, setting, get_proxy_mysql,re
config = setting.configs
url_db = config['url_db']
host = url_db['host']
user = url_db['user']
password = url_db['password']
db_name = url_db['database']
local_path = setting.save_path()
# print local_path
def apkhouse(data):
    url = data[1]
    print url
    s = requests.session()
    proxy = get_proxy_mysql.get_proxy()
    if proxy:
        s.proxies = proxy
    ress = s.get(url)
    re_com = re.compile(r'class="goog-inline-block jfk-button jfk-button-action" href="(.*?)">')
    url_down = re.search(re_com, ress.text).group(1).replace('amp;', '')
    urls = 'https://docs.google.com' + url_down
    print urls
    a = ress.text
    re_type = re.compile(r'<span class="uc-name-size"><a href="https://docs.google.com.*?">(.*?)</a>')
    file_type = re.search(re_type, a).group(1)[-4:]
    id = data[0]
    file_name = local_path + data[2] + file_type
    print file_name
    start = time.time()
    r = s.get(urls, stream=True)
    with open(file_name, "wb") as code:
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                code.write(chunk)
    end = time.time()
    used_time = end - start
    print '文件下载完成,用时%s秒' % used_time
    db = MySQLdb.connect(host,user, password, db_name)
    cursor = db.cursor()
    sql = 'update download set status=2,path="%s" where id=%s' % (file_name, id)
    try:
        cursor.execute(sql)
        db.commit()
        print '本地存储路径更新完成'
    except Exception, e:
        db.rollback()
        print str(e)