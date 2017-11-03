import random
import requests


class Download:
    """下载网页html"""
    def __init__(self):
        """
        创建一个随机的请求头
        """
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        ]
        self.head_connection = ['keep-alive']
        self.head_accept_language = ['zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3']
        self.head_accept = ['text/css,*/*;q=0.1']
        # self.ip_list = ip.get_ip_list()
        self.proxy = [
            '106.5.173.163:3276',
            '118.117.138.173:2645',
            '111.74.232.220:9756',
            '60.17.248.204:2121',
            '116.208.96.24:3154',
            '100.18.21.221:8110',
            '117.68.145.78:2644',
            '182.111.49.213:4162',
            '36.34.14.53:6436',
            '114.226.135.105:9287',
            '222.189.89.180:5638',
            '36.34.15.96:6436',
            '117.57.170.138:3852',
            '112.85.10.250:1131',
            '115.219.76.29:2316',
            '60.173.24.251:6890',
            '117.71.152.248:2319',
            '106.110.249.222:3456',
            '60.187.145.145:2315',
            '117.90.2.47:3217',
            '222.163.253.2:2862',
            '123.189.48.142:9706',
            '60.160.186.100:7654',
            '36.33.18.1:6436',
            '171.215.203.35:2645',
            '59.62.194.171:6344',
            '114.99.22.214:6890',
            '111.77.20.64:4162',
            '182.100.162.23:4162',
            '60.168.23.241:2644',
            '42.54.231.82:3529',
            '115.153.104.137:2314',
            '117.68.242.119:2644',
            '106.5.5.120:9756',
            '100.18.25.49:8110',
            '182.111.98.113:2314',
            '49.67.138.134:2137',
            '117.68.242.186:2644',
            '223.215.149.202:2319',
            '175.151.220.99:1767',
            '183.145.53.113:2315',
            '117.90.2.51:3217',
            '36.45.194.35:3215',
            '123.152.37.190:2682',
            '117.70.137.207:6436',
        ]

    def get_url(self, url, timeout, num_retries=3):
        """
        构造请求头，并获取响应
        :param url:
        :param timeout:
        :return:
        """
        UA = random.choice(self.user_agent_list)
        headers = {
            'Connection': self.head_connection[0],
            'Accept': self.head_accept[0],
            'Acccept-Language': self.head_accept_language[0],
            'Use-Agent': UA,
                   }
        ip = random.choice(self.proxy)
        proxies = {'http': ip}
        try:
            response = requests.get(url, timeout=timeout, headers=headers, proxies=proxies)
        except:
            print("获取网页出错")
            response = None
            if num_retries > 0:
                print('获取页面倒数第%s次' % num_retries)
                return self.get_url(url, timeout, num_retries-1)
        else:
            return response