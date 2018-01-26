#coding:utf8
import get_data_mysql,downloads.simple as simple,re
# 获取URL等信息,从数据库中
data = get_data_mysql.get_data()
print data
if data:
    def_name = data[1].split('/')[2]
    print def_name
    if data[1][-4] == '.':
        simple.simple(data)
    elif def_name == 'android-1.com':
        downloads.android(data)
    else:
        re_module = re.compile(r'.*?(\w+?)\.(com|cn|net|xin)')
        module_name = re.search(re_module,def_name)
        if module_name:
            module_name = module_name.group(1)
            # 引入相应模块
            import_name = 'import ' + 'downloads.' + module_name
            print import_name
            exec import_name
            # 调用相应函数
            do_def = 'downloads.' + module_name + '.' + module_name + '(data)'
            print do_def
            exec do_def
else:
    print '没取到数据'

