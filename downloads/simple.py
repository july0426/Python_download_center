#coding:utf8
import setting,download
def simple(data):
    local_path = setting.save_path()
    url = data[1]
    print url
    file_type = url[-4:]
    id = data[0]
    file_name = local_path + data[2] +file_type
    print file_name
    download.download(url,file_name,id)