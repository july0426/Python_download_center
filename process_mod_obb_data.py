#coding:utf8
'''
mod obb 数据处理
从pdts_mod_data_center 数据表中提取任务源
mod_center_proxy 代理表
提取代理
根据不同的任务来源进行数据处理
'''
import re,MySQLdb,requests,json,os,time,random,stat
from contextlib import closing
def get_proxies():
    db = MySQLdb.connect('localhost', 'mod_caicai_200', 'mod_caicai_pass', 'mod_process_center')
    cursor = db.cursor()
    sql = "select * from mod_center_proxy order by status asc limit 1"
    try:
        cursor.execute(sql)
        proxies = cursor.fetchone()
        # 更新代理时间戳
        sql = "update mod_center_proxy set status=%d where id=%d" % (int(time.time()), proxies[0])
        cursor.execute(sql)
        db.commit()
        db.close()
        proxy = {
            'http': 'http://%s' % proxies[2],
            'https': 'https://%s' % proxies[2],
        }
        return proxy
    except Exception, e:
        print " Get proxy Faild1 "
        db.rollback()
        db.close()
        return False
def get_a_metion_to_process():
    db = MySQLdb.connect('localhost', 'mod_caicai_200', 'mod_caicai_pass', 'mod_process_center')
    cursor = db.cursor()
    sql = "select id,app_url_id,download_mod_link,url from pdts_mod_data_center where obb_status=0 ORDER BY id DESC limit 1"
    try:
        cursor.execute(sql)
        the_job = cursor.fetchone()
        #更改状态
        sql = "update pdts_mod_data_center set obb_status=1 where id=%d " % the_job[0]
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return the_job
        except Exception, e:
            print " Change Metion Status Faild "
            db.close()
            return False
    except Exception, e:
        print "Process Done"
        db.close()
        return False
def make_save_path():
    #生成目录
    dir_array = ("q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b")
    apksavepath = "/home/wwwroot/2016_mod/"+dir_array[random.randint(0, 23)] + "/" + dir_array[random.randint(0, 23)] + "/" + dir_array[random.randint(0, 23)] + "/"
    # os.makedirs(paths)
    if os.path.exists(apksavepath):
        pass
    else:
        os.makedirs(apksavepath)
        os.chmod(apksavepath, stat.S_IRWXG|stat.S_IRWXU|stat.S_IRWXO)
    return apksavepath
def process_dropapk_url(data,apksavename,proxy):
    url = data[2]
    print url
    s = requests.session()
    datas = {
        'op': 'download2',
        'id': url.split('/')[-1],
        'rand': '',
        'referer': url,
        'method_free': 'Free Download',
        'method_premium': '',
        'adblock_detected': '0',
    }
    if proxy:
        s.proxies = proxy
        text = s.post(url,data = datas).text
    else:
        text = s.post(url,data = datas).text
    re_url = re.compile(r'<a href="(.*?)"><img src="https://dropapk.com/images_mega/down_final.png"')
    url = re.search(re_url,text)
    if url:
        url = url.group(1)
        file_type = url[-4:]
        file_name = apksavename + data[1] + file_type
        print file_name
        print url
        with closing(s.get(url, stream=True)) as r:
            with open(file_name, "wb") as code:
                for chunk in r.iter_content(chunk_size=1024000):
                    if chunk:
                        code.write(chunk)
        if os.path.exists(file_name):
            return file_name
        else:
            return False
    else:
        print 'dropapk.com Download Url Match Faild'
        return False
#drive.google.com 下载地址处理
def process_drive_google_url(the_job,save_path,proxy):
    url = the_job[2]
    s = requests.session()
    if proxy:
        s.proxies = proxy
    ress = s.get(url)
    re_com = re.compile(r'class="goog-inline-block jfk-button jfk-button-action" href="(.*?)">')
    url_down = re.search(re_com, ress.text)
    if url_down:
        urls = 'https://drive.google.com' + url_down.group(1).replace('amp;', '')
        a = ress.text
        re_type = re.compile(r'<span class="uc-name-size"><a href="https://drive.google.com.*?">(.*?)</a>')
        file_type = re.search(re_type, a).group(1)[-4:]
        file_name = save_path + the_job[1] + file_type
        print file_name
        with closing(s.get(urls, stream=True,proxies=proxy)) as r:
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

# apkhouse 下载地址处理
def process_apkhouse_url(the_job, save_path, proxy):
    url = the_job[2]
    s = requests.session()
    if proxy:
        s.proxies = proxy
    ress = s.get(url)
    request_url = ress.url
    if 'mobdisc.com' in request_url:
        print 'mobdisc Download Url'
        title = re.search(r'<title>(.*?)</title>', ress.text)
        if title:
            title = title.group(1)
        else:
            print 'Error 1'
            return
        file_type = title[-4:]
        print file_type
        re_id = re.compile(r'data-dwn="(\w+?)" rel="nofollow noopener"')
        file_id = re.search(re_id, ress.text)
        if file_id:
            file_id = file_id.group(1)
            post_data = {
                'dwn': file_id,
                'vr': 'false'
            }
            ress = requests.post('http://mobdisc.com/get_key/', data=post_data)
            if ress:
                pass
            else:
                print "Post mob Data Faild"
                return False
            link = json.loads(ress.text)["link"].replace('\\', '')
            url = 'http://mobdisc.com' + link
            if url:
                pass
            else:
                return False
            print url
            file_name = save_path + the_job[1] + file_type
            return download_data(url, file_name, proxy)
    elif 'docs.google.com' in request_url:
        re_com = re.compile(r'class="goog-inline-block jfk-button jfk-button-action" href="(.*?)">')
        url_down = re.search(re_com, ress.text).group(1).replace('amp;', '')
        urls = 'https://docs.google.com' + url_down
        print urls
        a = ress.text
        re_type = re.compile(r'<span class="uc-name-size"><a href="https://docs.google.com.*?">(.*?)</a>')
        file_type = re.search(re_type, a).group(1)[-4:]
        file_name = save_path + the_job[1] + file_type
        print file_name
        with closing(s.get(urls, stream=True, proxies=proxy)) as r:
            with open(file_name, "wb") as code:
                for chunk in r.iter_content(chunk_size=512000):
                    if chunk:
                        code.write(chunk)
        if os.path.exists(file_name):
            return file_name
        else:
            return False
    else:
        print "Unknow Download Url"
        return False

def process_filescdn_url(the_job, save_path, proxy):
    url = the_job[2]
    s = requests.session()
    if proxy:
        s.proxies = proxy
    res = s.get(url)
    re_rand = re.compile(r'name="rand" value="(.*)?">')
    rand = re.findall(re_rand, res.text)
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
            file_name = save_path + the_job[1] + file_type
            with closing(s.post(url, data=datas, stream=True)) as r:
                with open(file_name, "wb") as code:
                    for chunk in r.iter_content(chunk_size=512000):
                        if chunk:
                            code.write(chunk)
            if os.path.exists(file_name):
                return file_name
            else:
                return False
    else:
        print 'filescdn.com Download Faild'
        return False

#apptoko 网站 obb 下载
def process_apptoko_url(the_job,save_path,proxy):
    s = requests.session()
    if proxy:
        text = s.get(the_job[3], proxies=proxy).text
    else:
        text = s.get(the_job[3]).text
    version_id = the_job[2]
    post_data = {'version_id': version_id}
    text = s.post('https://apptoko.com/android/android/general_download', data=post_data).text
    re_url = re.compile(r'"download":"(.*?)"')
    urlss = re.search(re_url, text)
    if urlss:
        pass
    else:
        print " Mach Download Url Faild "
        return False
    urls = urlss.group(1).replace('\\', '')
    file_type = urls[-4:]
    file_name = save_path + the_job[1] + file_type
    print file_name
    print urls
    with closing(s.get(urls, stream=True)) as r:
        with open(file_name, "wb") as code:
            for chunk in r.iter_content(chunk_size=512000):
                if chunk:
                    code.write(chunk)
    if os.path.exists(file_name):
        return file_name
    else:
        return False
#upfiles.com网站obb下载
def process_upfiles_url(the_job,save_path,proxy):
    url = the_job[2]
    s = requests.session()
    if proxy:
        s.proxies = proxy
    ress = s.get(url)
    text = ress.text
    # print text
    re_token = re.compile(r'<input name="_token" type="hidden" value="(.*)?">')
    token = re.search(re_token,text)
    re_file_type = re.compile(r'<title>(.*)?\|.*</title>')
    if token:
        token = token.group(1)
        file_type = re.search(re_file_type,text).group(1).replace(' ','')[-4:]
        post_data = {"_token":token}
        file_name = save_path + the_job[1] + file_type
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
        print 'upfiles.com Download Url Match Faild'
        return False

'''根据传入的URL,下载文件,返回文件存储地址'''
def download_data(url,file_name,proxy):
    with closing(requests.get(url, stream=True,proxies=proxy)) as r:
        with open(file_name, "wb") as code:
            for chunk in r.iter_content(chunk_size=512000):
                if chunk:
                    code.write(chunk)
    if os.path.exists(file_name):
        return file_name
    else:
        return False
def write_data_to_apk_system(appurlid,path):
    db = MySQLdb.connect('localhost', 'evzcai200', 'evzcai200_pass', 'apk_system_20161228')
    cursor = db.cursor()
    sql = " insert into pdts_host_info (status,url_id,apk_save_path,verify_status,email_status,source) values (%d,'%s','%s',%d,%d,%d) " % (1000,appurlid,path,111,int(time.time()),7)
    try:
        cursor.execute(sql)
        db.commit()
        print " Insert Success "
        db.close()
        return True
    except Exception, e:
        print " Insert Faild "
        db.close()
        return False
def change_download_status( ids,status ):
    db = MySQLdb.connect('localhost', 'mod_caicai_200', 'mod_caicai_pass', 'mod_process_center')
    cursor = db.cursor()
    sql = "update pdts_mod_data_center set obb_status=%d where id=%d " % ( status,ids )
    try:
        cursor.execute(sql)
        db.commit()
        print " Update acmarket_pdts Success "
        db.close()
        return True
    except Exception, e:
        print " Faild To Update "
        db.close()
        return False
#提取下载任务
the_job = get_a_metion_to_process()
if the_job == False:
    print " No Job Need To Process "
    exit()
proxy = get_proxies()
save_path = make_save_path()
print the_job[0]
#判断下载链接 类型
if "dropapk.com" in the_job[2]:
    savepath = process_dropapk_url(the_job,save_path,proxy)
elif "apkhouse.com" in the_job[2]:
    savepath = process_apkhouse_url(the_job,save_path,proxy)
elif 'upfiles.co' in the_job[2]:
    save_path = process_upfiles_url(the_job,save_path,proxy)
elif 'filescdn' in the_job[2]:
    save_path = process_filescdn_url(the_job,save_path,proxy)
elif "apptoko.com" in the_job[3]:
    savepath = process_apptoko_url(the_job,save_path,proxy)
elif ".zip" in the_job[2]:
    file_name = save_path + the_job[1] + ".zip"
    print file_name
    savepath = download_data(the_job[2],file_name,proxy)
elif ".apk" in the_job[2]:
    file_name = save_path + the_job[1] + ".apk"
    print file_name
    savepath = download_data(the_job[2],file_name,proxy)
elif ".rar" in the_job[2]:
    file_name = save_path + the_job[1] + ".rar"
    print file_name
    savepath = download_data(the_job[2],file_name,proxy)
elif 'drive.google.com' in the_job[2]:
    new_url = the_job[2].replace('open','uc') + '&export=download'
    the_job[2] = new_url
    savepath = process_drive_google_url(the_job,save_path,proxy)

# elif "" in the_job[2]:

# elif "" in the_job[2]:
else:
    savepath = ''
    print " Unknow Download Url Type "

if savepath:
    status = int(time.time())
else:
    status = -12
#更新数据库状态
if status > 10:
    write_data_to_apk_system(the_job[1],savepath)

change_download_status(the_job[0],status)