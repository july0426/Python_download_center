#coding:utf8
import requests,time,MySQLdb, setting, get_proxy_mysql,re,download
config = setting.configs
url_db = config['url_db']
host = url_db['host']
user = url_db['user']
password = url_db['password']
db_name = url_db['database']
local_path = setting.save_path()
def directapk(data):
    url = data[1]
    print url
    # proxy = get_proxy_mysql.get_proxy()
    proxy = 0
    s = requests.session()
    if proxy:
        text = s.get(url, proxies=proxy).text
    else:
        text = s.get(url).text
    re_url = re.compile(r"<a class='btn btn-default-dl' href='(.*?)'>download now</a>")
    url = re.search(re_url, text)
    re_type = re.compile(r'File:(.*?)<br/>')
    file_type = re.search(re_type, text)
    if url:
        if file_type:
            urls = url.group(1)
            print urls
            file_type = file_type.group(1).strip()[-4:]
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
    else:
        print 'android网站,未匹配到下载的URL'
