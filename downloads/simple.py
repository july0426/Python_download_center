#coding:utf8
import setting,download
def simple(data):
    obbsave_path = setting.savepath
    url = data[1]
    print url
    file_type = url[-4:]
    id = data[0]
    if os.path.exists(obbsave_path):
        pass
    else:
        os.makedirs(obbsave_path)
        os.chmod(obbsave_path, stat.S_IRWXG | stat.S_IRWXU | stat.S_IRWXO)
    file_name = obbsave_path + data[2] +file_type
    print file_name
    download.download(url,file_name,id)