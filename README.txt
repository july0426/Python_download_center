obb安装包下载中心
<<<<<<< HEAD
get_data_mysql.py:  连接数据库,取出任务,包括URL等数据
get_proxy_mysql.py: 链接数据库,取出代理
setting.py:         设置数据库参数,本地文件存储路径,并随机创建文件夹
manage.py:          处理中心,根据数据库取出的数据,调用对应的下载模块,运行这个文件就可以.
download.py:        文件下载,分块写入到本地,并把路径存入数据库中
downloads(dir):     这个文件夹下面是不同网站的下载模块,文件名和里面函数名要跟目标网站的域名一致,
                    例如网站:http://www.directapk.net 文件名和函数名就都是directapk
                    其中simple是针对那些URL就是最终下载路径的,直接调用他就可以完成下载.
                    后续有其他需求,在这里面写新的文件就可以


            1.谷歌人机识别,暂时攻不破

            https://uplod.ws/6dr1j504dqlo

            https://uplod.it/m8dmh2xl6wsr

            https://uplod.cc/0g7sfauecd79

            https://dailyuploads.net/vx4khlfp3czt

            https://douploads.com/x11xpp7w3avo



            2.https://uploads.to/y2vchqm3fxhk

            共有2条,网页显示文件不存在



            3.这个网站的就3条

            https://racaty.com/89er26gyf61x

            https://racaty.com/2sxqk32euox4

            https://racaty.com/xe2xhub7x609



            4.下面是真是的下载链接,最后/后面的是文件名字,自己写什么都可以,前面的是重要的

            http://srv1.racaty.com:182/d/qqfmir3f6xjz7x5isokzz62iz2aolaksd2tsdyhy2d6p4nuwwmqzlmmrnft3gvz6wdnq5fp3/com.gameloft.android.ANMP.GloftOLHM.zip



            5.https://androidrepublic.org/forum/threads/the-obb-trick-tutorial.4552/

            是教程的链接,不是下载链接



            6.https://userscloud.com/gm2ol2898lmz

            需要注册,收费,还需要提供信用卡  共17条



            7.dl1.revdownload.com/dl1/1701/Asphalt_8_Airborne_v3.3.1a_Mod__7720_Revdl.com.apk

            http://dl1.revdownload.com   这个网站,有5条,应该是网络的问题导致下载中断,是可以直接下载的



            8.https://drive.google.com/open?id=0B7YOVZ25i4rILTNibTJVUTgyTmc

            这个打不开,显示权限不够



            9.https://drive.google.com/open?id=0B6LFIl3CgPkCakplM1pUZ3NIeXM

            这种链接,要更换城下面的链接,以谷歌云盘的方式下载

            https://drive.google.com/uc?id=0B6LFIl3CgPkCakplM1pUZ3NIeXM&export=download






改版后决定采用wget来下载文件
wget 非常稳定,它在带宽很窄的情况下和不稳定网络中有很强的适应性.
如果是由于网络的原因下载失败，wget会不断的尝试，直到整个文件下载完毕。
如果是服务器打断下载过程，它会再次联到服务器上从停止的地方继续下载。
这对从那些限定了链接时间的服务器上下载大文件非常有用。
wget -c  -q -O %s --user-agent="%s"  %s' % (file_name,user_agent,url
-c  断点续传    -d  –debug 打印调试输出
-q  –quiet 安静模式(没有输出)
-U, –user-agent=AGENT 设定代理的名称为 AGENT而不是 Wget/VERSION
-O 指定的输出文件,不指定就默认当前目录下
$path = "wget -e use_proxy=yes -e 'https_proxy={$proxy}' -c -d -q -O $save_name --user-agent=$user_agent  \"$url\"  &";
$path = "wget -e use_proxy=yes -e 'http_proxy={$proxy}' -c -d -q -O $save_name --user-agent=$user_agent  \"$url\"  &"; 这个是http 的代理
=======
get_data_mysql是连接数据库,取出任务,包括URL等数据
get_proxy_mysql是链接数据库,取出代理
setting:设置数据库参数,本地文件存储路径,并随机创建文件夹
manage:处理中心,根据数据库取出的数据,调用对应的下载模块,运行这个文件就可以.
downloads:这个文件夹下面是不同网站的下载模块,文件名和里面函数名要跟目标网站的域名一致,
          例如网站:http://www.directapk.net 文件名和函数名就都是directapk
          其中simple是针对那些URL就是最终下载路径的,直接调用他就可以完成下载.
          后续有其他需求,在这里面写新的文件就可以
>>>>>>> 81174ef2a332689612667f84d56226b4acc88b85
