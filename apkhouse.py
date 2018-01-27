#coding:utf8
import requests,time,MySQLdb, setting, get_proxy_mysql,re,download,json
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
    request_url = ress.url
    if 'mobdisc.com' in request_url:
        print '这个安装包在mobdisc上'
        title = re.search(r'<title>(.*?)</title>', ress.text)
        if title:
            title = title.group(1)
        else:
            print '页面不对劲'
            return
        file_type = title[-4:]
        print file_type
        id = data[0]
        re_id = re.compile(r'data-dwn="(\w+?)" rel="nofollow noopener"')
        file_id = re.search(re_id, ress.text)
        if file_id:
            file_id = file_id.group(1)
            post_data = {
                'dwn': file_id,
                'vr': 'false'
            }
            ress = requests.post('http://mobdisc.com/get_key/', data=post_data)
            print ress.text
            link = json.loads(ress.text)["link"].replace('\\', '')
            url = 'http://mobdisc.com' + link
            print url
            file_name = local_path + data[2] + file_type
            download.download(url, file_name, id)
    elif 'docs.google.com' in request_url:
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