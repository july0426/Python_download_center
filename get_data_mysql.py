#coding:utf8
import requests,time,MySQLdb,setting,get_proxy_mysql
config = setting.configs
'''链接数据库,取出URL及文件名称'''
def get_data():
    url_db = config['url_db']
    host = url_db['host']
    user = url_db['user']
    password = url_db['password']
    db_name = url_db['database']
    db = MySQLdb.connect(host,user,password, db_name)
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
            return record
        else:
            return 0
    except Exception, e:
        db.rollback()
        print str(e)