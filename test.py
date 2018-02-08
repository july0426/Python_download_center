#:coding:utf8
import requests,re
from contextlib import closing
url = 'https://filescdn.com/7wpm28s9egg1'
# url = 'https://filescdn.com/tt2mu0wssor9'
s = requests.session()

res = s.get(url)
print res.text
re_rand = re.compile(r'name="rand" value="(.*)?">')
rand = re.findall(re_rand,res.text)
print rand
if len(rand)>1:
    rand = rand[1]
    id = url.split('/')[-1]
    data = {
        "op":"download2",
        "id":id,
        "rand":rand,
        "referer":"http://mirrorclouds.com/dl.php?url="+url,
        "method_free":"",
        "method_premium":""
        }
    re_file_type = re.compile(r'<Title>(.*)?</Title>')
    file_type = re.search(re_file_type,res.text)
    if file_type:
        file_type = '.' + file_type.group(1)[-3:]
        print file_type
        print data
        file_name = '/users/qiyue/myxuni/pngtree/obb_download/' + 'filescdn.zip'
        print file_name
        with closing(s.post(url, data=data, stream=True)) as r:
            with open(file_name, "wb") as code:
                for chunk in r.iter_content(chunk_size=512000):
                    if chunk:
                        code.write(chunk)

    # c = s.post('https://quaves.info/cUxnZFpecwQXZxI2PREXJgokJWtJDjEhFCUIIQALIzshPhgdCiNCLhgoWlJtR3pfUXwBJQNZa1c/EwUuBD9aU2JXJQkCNUxqEVlrX31XSm1HYlNCLgEtAFlrVxNaVW9Ae19UaEF7UF1sQQ')
    # d = s.get(url)
    # print d.text
    # # print b.text