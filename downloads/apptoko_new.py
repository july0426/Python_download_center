
s = requests.session()
if proxy:
    text = s.get(url, proxies=proxy).text
else:
    text = s.get(url).text
version_id =
post_data = {'version_id': version_id}
text = s.post('https://apptoko.com/android/android/general_download', data=post_data).text
print text
re_url = re.compile(r'"download":"(.*?)"')
urlss = re.search(re_url, text)
if urlss:
    urls = urlss.group(1).replace('\\', '')
    print urls
    file_type = urls[-4:]
    id = data[0]
    file_name = local_path + data[2] + file_type
    print file_name
    start = time.time()
    r = s.get(urls, stream=True)
    with open(file_name, "wb") as code:
        for chunk in r.iter_content(chunk_size=512000):
            if chunk:
                code.write(chunk)
    db = MySQLdb.connect(host, user, password, db_name)
    cursor = db.cursor()
    sql = 'update download set status=2,path="%s" where id=%s' % (file_name, id)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception, e:
        db.rollback()
        print str(e)
