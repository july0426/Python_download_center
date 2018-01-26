#coding:utf8
import requests,time,MySQLdb,setting,get_proxy_mysql
config = setting.configs
url_db = config['url_db']
host = url_db['host']
user = url_db['user']
password = url_db['password']
db_name = url_db['database']
'''根据传入的URL,下载文件,并将文件路径保存到数据库'''
def download(url,file_name,id):
    db = MySQLdb.connect(host,user, password, db_name)
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
    with open(file_name, "wb") as code:
        try:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    code.write(chunk)
        except Exception as e:
            print '下载失败:',str(e)
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