#coding:utf-8
import os,subprocess,MySQLdb,random,stat
host = 'localhost'
user = 'root'
password = '123456'
db_name = 'test'
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
        proxy = proxies[1]
        db.commit()
        return proxy
    except Exception, e:
        print sql
        print str(e)
        db.rollback()
        proxy = 0
        return proxy
def get_data():
    db = MySQLdb.connect(host,user,password, db_name)
    cursor = db.cursor()
    sql = 'SELECT id,url,name from download where status=0 and url like "%apkhouse.com%" limit 1'
    try:
        cursor.execute(sql)
        record = cursor.fetchone()
        db.commit()
        if record:
            sql = 'update download set status=1 where id=%s' % record[0]
            try:
                cursor.execute(sql)
                db.commit()
            except Exception, e:
                db.rollback()
                print str(e)
            return record
        else:
            return 0
    except Exception, e:
        db.rollback()
        print str(e)
    db.close()
def user_agent_random():
    user_agent_list = [
        'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'User-Agent:Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
        'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)',
        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',
    ]
    return random.choice(user_agent_list)
def get_save_path():
    loacl_path = '/users/qiyue/myxuni/pngtree/Python_download_center/'
    dir_array = ("q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v","b")
    savepath = loacl_path + random.choice(dir_array) + "/" + random.choice(dir_array) + "/" + random.choice(dir_array) + "/"
    if os.path.exists(savepath):
        pass
    else:
        os.makedirs(savepath)
        os.chmod(savepath, stat.S_IRWXG | stat.S_IRWXU | stat.S_IRWXO)
    # print savepath
    return savepath
def download():
    data = get_data()
    if data:
        id = data[0]
        url = data[1]
        file_type = url[-4:]
        save_path = get_save_path()
        print save_path
        file_name = save_path + data[2] + file_type
        user_agent = user_agent_random()
        commond = 'wget -c -q -O %s --user-agent="%s"  "%s"' % (file_name,user_agent,url)
        # 加代理版
        # proxy = get_proxy()
        # commond = 'wget -e use_proxy=yes -e "http_proxy={%s}" -c -q -O %s --user-agent="%s"  "%s"' % (proxy,file_name,user_agent,url)
        print commond
        # subprocess.call(commond, shell=True)
        try:
            subprocess.check_call(commond, shell=True)
        except subprocess.CalledProcessError as err:
            print("Command Error")
        if os.path.exists(file_name):
            db = MySQLdb.connect(host, user, password, db_name)
            cursor = db.cursor()
            sql = 'update download set status=2,path="%s" where id=%s' % (file_name, id)
            try:
                cursor.execute(sql)
                db.commit()
                print 'savepath update sucess'
            except Exception, e:
                db.rollback()
                print str(e)
download()