#coding:utf8
import requests,time,MySQLdb,re,json,os
from contextlib import closing
'''从数据库提取代理'''
def get_proxy():
    db = MySQLdb.connect('localhost', 'root', '123456', 'test')
    cursor = db.cursor()
    sql = "select * from pngtree_proxy order by status asc limit 1"
    try:
        cursor.execute(sql)
        proxies = cursor.fetchone()
        # 更新代理时间戳
        sql = "update pngtree_proxy set status=%d where id=%d" % (int(time.time()), proxies[0])
        cursor.execute(sql)
        proxy = {
            'http': 'http://%s' % proxie,
            'https': 'https://%s' % proxie,
        }
        db.commit()
        return proxy
    except Exception, e:
        print sql
        print str(e)
        db.rollback()
        proxy = 0
        return proxy
'''根据传入的URL,下载文件,并将文件路径保存到数据库'''
def download(url,file_name,id):
    db = MySQLdb.connect('localhost', 'root', '123456', 'test')
    cursor = db.cursor()
    start = time.time()
    # proxy = get_proxy()
    proxy = 0
    if proxy:
        r = requests.get(url, stream=True,proxies=proxy)
    # 采用流式请求,对内容进行迭代
    else:
        r = requests.get(url, stream=True)
    # 分块写入文件
    with closing(requests.get(url, stream=True)) as r:
        with open(file_name, "wb") as code:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    code.write(chunk)
    end = time.time()
    used_time = end - start
    print '文件下载完成,用时%s秒' % used_time
    sql = 'update download set status=2,path="%s" where id=%s' % (file_name,id)
    try:
        cursor.execute(sql)
        db.commit()
        print '本地存储路径更新完成'
    except Exception, e:
        db.rollback()
        print str(e)
    db.close()
def process_drive_google_url(the_job):
    url = the_job[1]
    s = requests.session()
    ress = s.get(url)
    re_com = re.compile(r'class="goog-inline-block jfk-button jfk-button-action" href="(.*?)">')
    url_down = re.search(re_com, ress.text)
    if url_down:
        urls = 'https://drive.google.com' + url_down.group(1).replace('amp;', '')
        print urls
        a = ress.text
        re_type = re.compile(r'<span class="uc-name-size"><a href="https://drive.google.com.*?">(.*?)</a>')
        file_type = re.search(re_type, a).group(1)[-4:]
        file_name = '/Users/qiyue/myxuni/pngtree/obb_download/download_dir/' + the_job[2] + file_type
        print file_name
        with closing(s.get(urls, stream=True)) as r:
            with open(file_name, "wb") as code:
                for chunk in r.iter_content(chunk_size=512000):
                    if chunk:
                        code.write(chunk)
        if os.path.exists(file_name):
            return file_name
        else:
            return False
    else:
        return False
def apkhouse(data):
    url = data[1]
    print url
    s = requests.session()
    proxy = get_proxy()
    if proxy:
        s.proxies = proxy
    ress = s.get(url)
    print ress.text,ress.url
    request_url = ress.url
    if 'mobdisc.com' in request_url:
        print '这个安装包在mobdisc上'
        title = re.search(r'<title>(.*?)</title>',ress.text)
        if title:
            title = title.group(1)
        else:
            print '页面不对劲'
            return
        file_type = title[-4:]
        print file_type
        id = data[0]
        re_id = re.compile(r'data-dwn="(\w+?)" rel="nofollow noopener"')
        file_id = re.search(re_id,ress.text)
        if file_id:
            file_id = file_id.group(1)
            post_data = {
                'dwn': file_id,
                'vr':'false'
            }
            ress = requests.post('http://mobdisc.com/get_key/',data = post_data)
            print ress.text
            link = json.loads(ress.text)["link"].replace('\\','')
            url = 'http://mobdisc.com' + link
            print url
            file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
            download(url, file_name, id)

    elif 'docs.google.com' in request_url:
        print '谷歌的云盘'
        re_com = re.compile(r'class="goog-inline-block jfk-button jfk-button-action" href="(.*?)">')
        url_down = re.search(re_com, ress.text).group(1).replace('amp;', '')
        urls = 'https://docs.google.com' + url_down
        print urls
        a = ress.text
        re_type = re.compile(r'<span class="uc-name-size"><a href="https://docs.google.com.*?">(.*?)</a>')
        file_type = re.search(re_type, a).group(1)[-4:]
        id = data[0]
        file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
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
        db = MySQLdb.connect('localhost', 'root', '123456', 'test')
        cursor = db.cursor()
        sql = 'update download set status=2,path="%s" where id=%s' % (file_name, id)
        try:
            cursor.execute(sql)
            db.commit()
            print '本地存储路径更新完成'
        except Exception, e:
            db.rollback()
            print str(e)
def zippyshare(data):
    url = data[1]
    print url
    proxy = get_proxy()
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
        file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
        print file_name
        download(url,file_name,id)
def revdl(data):
    url = data[1]
    print url
    proxy = 0
    if proxy:
        res = requests.get(url,proxies=proxy)
    else:
        res = requests.get(url)
    text = res.text
    re_url = re.compile(r'<a href="(.*)?" target="_blank"><li class="download">Go to Download Page</li></a>')
    url_data = re.search(re_url,text)
    if url_data:
        url_data = url_data.group(1)
        print url_data
        # try:
        res = requests.get(url_data)
        re_url = re.compile(r'<a href="(.*)?"><li class="download"><span>Download Apk</span></li></a>')
        url = re.search(re_url, res.text)
        if url:
            url = url.group(1)
            print url
            file_type = url[-4:]
            id = data[0]
            file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
            print file_name
            download(url, file_name, id)
        else:
            print 'revdl.com Download url Match Faild'
            return False
        # except Exception as e:
        #     print str(e)
        #     return False


def android(data):
    url = data[1]
    print url
    proxy = get_proxy()
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
            file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
            print file_name
            download(url,file_name,id)
    else:
        print 'android网站,未匹配到下载的URL'
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
    proxy = get_proxy()
    if proxy:
        text = requests.post(url,data = datas,proxies=proxy).text
    else:
        text = requests.post(url,data = datas).text
    re_url = re.compile(r'<a href="(.*?)"><img src="https://dropapk.com/images_mega/down_final.png"')
    url = re.search(re_url,text)
    if url:
        url = url.group(1)
        file_type = url[-4:]
        id = data[0]
        file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
        print file_name
        download(url,file_name,id)
    else:
        print 'dropapk.com网站的下载链接没有匹配到'
def userscloud(data):
    url = data[1]
    print url
    text = requests.get(url).text
    print text
    re_url = re.compile(r'<a href="(.*)?" data-toggle=".*?" data-title')
    url = re.search(re_url,text)
    if url:
        url = url.group(1)
        file_type = url[-4:]
        id = data[0]
        file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
        print file_name
        download(url,file_name,id)
    else:
        print 'serscloud网站的下载链接没有匹配到'
def filescdn(data):
    url = data[1]
    print url
    s = requests.session()
    res = s.get(url)
    print res.text
    re_rand = re.compile(r'name="rand" value="(.*)?">')
    rand = re.findall(re_rand, res.text)
    print rand
    if len(rand) > 1:
        rand = rand[1]
        id = url.split('/')[-1]
        datas = {
            "op": "download2",
            "id": id,
            "rand": rand,
            "referer": "http://mirrorclouds.com/dl.php?url=" + url,
            "method_free": "",
            "method_premium": ""
        }
        re_file_type = re.compile(r'<Title>(.*)?</Title>')
        file_type = re.search(re_file_type, res.text)
        if file_type:
            file_type = '.' + file_type.group(1)[-3:]
            print file_type
            print data
            file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
            print file_name
            with closing(s.post(url, data=datas, stream=True)) as r:
                with open(file_name, "wb") as code:
                    for chunk in r.iter_content(chunk_size=512000):
                        if chunk:
                            code.write(chunk)
            if os.path.exists(file_name):
                return file_name
            else:
                return False
def upfiles(data):
    url = data[1]
    print url
    s = requests.session()
    text = s.get(url).text
    # print text
    re_token = re.compile(r'<input name="_token" type="hidden" value="(.*)?">')
    token = re.search(re_token,text)
    re_file_type = re.compile(r'<title>(.*)?\|.*</title>')
    if token:
        token = token.group(1)
        file_type = re.search(re_file_type,text).group(1).replace(' ','')[-4:]
        post_data = {"_token":token}
        print post_data,file_type
        file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
        print file_name
        with closing(s.post(url,data=post_data,stream=True)) as r:
            with open(file_name, "wb") as code:
                for chunk in r.iter_content(chunk_size=512000):
                    if chunk:
                        code.write(chunk)
        if os.path.exists(file_name):
            return file_name
        else:
            return False
        id = data[0]
    else:
        print 'dropapk.com网站的下载链接没有匹配到'
def directapk(data):
    url = data[1]
    print url
    # proxy = get_proxy()
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
            file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
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
            db = MySQLdb.connect('localhost', 'root', '123456', 'test')
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
def apptoko(data):
    url = data[1]
    print url
    # proxy = get_proxy()
    proxy = 0
    s = requests.session()
    if proxy:
        text = s.get(url, proxies=proxy).text
    else:
        text = s.get(url).text
    re_id = re.compile(r'<option value="(\w+?)">.*?</option>')
    version_id = re.search(re_id, text)
    if version_id:
        version_id = version_id.group(1)
        print version_id
        post_data = {'version_id':version_id}
        text = s.post('https://apptoko.com/android/android/general_download',data=post_data).text
        print text
        re_url = re.compile(r'"download":"(.*?)"')
        urlss = re.search(re_url, text)
        if urlss:
            urls = urlss.group(1).replace('\\','')
            print urls
            file_type = urls[-4:]
            id = data[0]
            file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] + file_type
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
            db = MySQLdb.connect('localhost', 'root', '123456', 'test')
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
        print 'apptoko网站,未匹配到下载的URL'
def simple_download(data):
    url = data[1]
    print url
    file_type = url[-4:]
    id = data[0]
    file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + data[2] +file_type
    print file_name
    download(url,file_name,id)
'''链接数据库,取出URL及文件名称'''
def get_data():
    db = MySQLdb.connect('localhost', 'root', '123456', 'test')
    cursor = db.cursor()
    sql = 'select id,url,name from download where status=0 limit 1'
    try:
        cursor.execute(sql)
        record = cursor.fetchone()
        db.commit()
        if record:
            sql = 'update download set status=1 where id=%s' % record[0]
            # try:
            #     cursor.execute(sql)
            #     db.commit()
            # except Exception, e:
            #     db.rollback()
            #     print str(e)
            # print record
            return record
        else:
            return 0
    except Exception, e:
        db.rollback()
        print str(e)


if __name__ == '__main__':
    # 获取要下载的链接,从数据库中
    data = get_data()
    # 根据取出的URL,获取到网站名称,根据网站名称,调用相应的函数进行处理,下载文件
    if data:
        def_name = data[1].split('/')[2]
        print def_name
        if def_name == 'apkhouse.com':
            apkhouse(data)
        elif def_name == 'www101.zippyshare.com':
            zippyshare(data)
        elif def_name == 'android-1.com':
            android(data)
        elif def_name == 'dropapk.com':
            dropapk(data)
        elif def_name == 'www.dl.farsroid.com':
            simple_download(data)
        elif def_name == 'www.directapk.net':
            directapk(data)
        elif def_name == 'download.directapk.net':
            if data[1][-4] == '.':
                simple_download(data)
            else:
                print 'url跟预期不一样,无法下载'
        elif def_name == 'apptoko.com':
            apptoko(data)
        elif def_name == 'www.revdl.com':
            revdl(data)
        elif def_name == 'filescdn.com':
            filescdn(data)
        elif 'drive.google.com' in def_name:
            new_url = data[1].replace('open', 'uc') + '&export=download'
            data = list(data)
            data[1] = new_url
            print data
            savepath = process_drive_google_url(data)
        elif  def_name == 'upfiles.co':
            upfiles(data)

        else:
            print 'url不在该脚本处理范围内'
    else:
        print '没取到数据'

