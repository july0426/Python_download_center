#coding:utf8
import requests,time,MySQLdb,re
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
