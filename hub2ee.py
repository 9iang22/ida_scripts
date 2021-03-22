#!/usr/bin/python3
#encoding=utf8

import getopt
import sys
import requests
import json
import re
import os

check_dup_url = "https://gitee.com/projects/check_project_duplicate?import_url="
check_pri_url = "https://gitee.com/projects/check_project_private?import_url="

test_urls = ["https://github.com/ReFirmLabs/binwalk",
        "https://github.com/attify/firmware-analysis-toolkit",
        "https://github.com/Mosk0ng/ida_scripts"]

cookie ={
    # your cookie there
}

def get_cookie():
    pass

def check_dup(url,cookie):
    res = requests.get(url=check_dup_url+url, cookies=cookie)
    data = json.loads(res.text)
    if(data["is_duplicate"]):
        msg = data["message"].encode("utf8")
        start = msg.find('<a href="')
        end = msg.find('"',start+len('<a href="'))
        return msg[(start+len('<a href="')):end]
    return None

def check_pri(url,cookie):
    res = requests.get(url=check_pri_url+url, cookies=cookie)
    data = json.loads(res.text)
    return data["check_success"]

def check_urls(urls, cookie):
    res = {}
    print("")
    print("----------------START CHECK---------------")
    print("")
    for url in urls:
        gitee_url = check_dup(url,cookie)
        if(gitee_url):
            if(check_pri(url,cookie)):
                print("GITHUB: %s\nGITEE: %s\n" % (url,gitee_url))
                res[url] = gitee_url
            else:
                print("GITHUB: %s\nGITEE(PRIVATE): %s\n" % (url,gitee_url))
                res[url] = url
        else:
            print("GITHUB: %s\nNOT FOUND\n" % (url))
            res[url] = url
    return res

def load_file(filename):
    with open(filename) as f:
        sh = f.read()
    return sh

def save_file(filename,sh):
    with open("fix_" + filename, "w") as f:
        f.write(sh)
    print("")
    print("----------------DO DIFF--_---------------")
    print("")
    os.system("diff %s %s" % (filename,"fix_"+filename))


def fix_file(filename):
    sh = load_file(filename)
    pattern = re.compile('git clone https://github.+')
    res = re.findall(pattern,sh)
    urls = []
    prefix = len("git clone ")
    for r in res:
        urls.append(r[prefix:])
    print("")
    print("----------------GITHUB URLS---------------")
    print("")
    for url in urls:
        print(url)
    gitee_urls = check_urls(urls,cookie)
    for url in urls:
        sh = re.sub(url,gitee_urls[url],sh)
    save_file(filename,sh)

def help():
    print("[*] Help info")
    print("Usage:fuck.py [OPTION]...")
    print("\t-u --url\t\tfind mirrors on gitee")
    print("\t-f --filepath\t\treplaces all github url to gitee's if there is a mirros")

if __name__ == "__main__":
    opts,args = getopt.getopt(sys.argv[1:],'-h-f:-u:',['help','filepath','url'])
    #print(opts)
    for opt_name,opt_value in opts:
        if opt_name in ('-h','--help'):
            help()
            sys.exit()
        if opt_name in ('-f','--filepath'):
            fix_file(opt_value)
            sys.exit()
        if opt_name in ('-u','--url'):
            fileName = opt_value
            print("[*] Filename is ",fileName)
            urls = [opt_value]
            check_urls(urls)
            sys.exit()
    help()
    sys.exit()
        




