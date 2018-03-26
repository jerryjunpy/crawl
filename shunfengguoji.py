# -*- coding: utf-8 -*-
import random
import requests
import time
import redis
import json
import threading
import datetime


class Download:
    """下载网页html"""
    def __init__(self):
        """
        创建一个随机的请求头
        """
        self.user_agent_list = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) "
            "CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",

            "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; m1 metal Build/LMY47I) AppleWebKit/537.36 "
            "(KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36",

            "Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 5.1.1)",

            "Mozilla/5.0 (Linux; Android 6.0; MP1512 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.4 (Baidu; P1 6.0)",

            "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; X9007 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko)"
            "Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36",

            "Mozilla/5.0 (iPhone 6s; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) "
            "Version/10.0 MQQBrowser/7.6.0 Mobile/14E304 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",

            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; vivo Xplay6 Build/MXB48T) AppleWebKit/537.36 "
            "(KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36",

            "Mozilla/5.0 (Linux; Android 6.0.1; SM-A9000 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 6.0.1)",

            "Mozilla/5.0 (Linux; Android 6.0.1; vivo X9Plus Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 6.0.1)",

            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 "
            "(KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.9 NetType/WIFI Language/zh_C",

            "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11t Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043307 Safari/537.36 "
            "MicroMessenger/6.5.8.1060 NetType/WIFI Language/zh_CN",

            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) "
            "CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",

            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko)"
            "Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.1 Mobile Safari/537.36",
        ]
        self.redis_client = redis.Redis(host='192.168.3.83', port=6379)

        self.shunfeng_url = 'https://www.trackingmore.com/gettracedetail.php?lang=cn&callback=' \
                         'jQuery17105806801095112044_1521165921825&tracknumber='

        self.bash_url = '&express=sf-express&pt=0&tracm=&destination=&exception=0&_=1521165988944'

    def get_url(self, timeout):
        """
        通邮挂号，trackingmore
        构造请求头，并获取响应
        :param url:
        :param timeout:
        :return:
        """

        while True:

            shunfeng = self.redis_client.spop('shunfeng_url')
            # laowo = 'RB023076373LA'

            if shunfeng:

                tracking_number = (str(shunfeng, encoding="utf-8"))

                self.download_data(tracking_number)
           
           else:
                
                break

    def download_data(self, tracking_number, num_tries=5):

        UA = random.choice(self.user_agent_list)

        shunfeng_url = self.shunfeng_url + tracking_number + self.bash_url  # 网址

        referer = 'https://www.trackingmore.com/sf-express-tracking/cn.html'

        headers = {
            'Host': 'www.trackingmore.com',
            'Connection': 'keep-alive',
            'Accept': '* / *',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'referer': referer,
            'user-agent': UA,
            }
        
        try:
            response = requests.get(shunfeng_url, timeout=10, headers=headers,)

        except Exception as e:

            print("获取数据%s出错" % tracking_number)
            print(e)

            num_tries -= 1  # 重新获取数据次数

            if num_tries > 0:
                
                self.download_data(tracking_number, num_tries)  # 获取网页失败重新再获取

        else:

            try:
                a = response.text

                b = a.lstrip('\tjQuery17105806801095112044_1521165921825').lstrip('(').rstrip(')')

                j = json.loads(b)

                trackinfo = j['originCountryData']['trackinfo'][0]

            except:

                print('无法识别的物流单号%s' % tracking_number)

                self.redis_client.sadd('shunfeng_absent', tracking_number)

            else:

                print(j['originCountryData']['trackinfo'])

                j['nu'] = tracking_number

                self.redis_client.lpush('shuefeng_item', j)

            seconds = [0.6, 0.8, 1.0, 1.2, 1.3, 1.6, 1.5, 1.7, 1.8, 1.9, 2.0, 2.2, 2.4, 2.8, 2.9,
                       3.0, 3.4, 3.2, 2.5]

            time.sleep((random.choice(seconds)))

    def run(self):

        thread_list = []
        try:
            # 创建一个线程，并指定执行的任务
            t1 = threading.Thread(target=self.get_url, args=[8])
            t2 = threading.Thread(target=self.get_url, args=[8])
            t3 = threading.Thread(target=self.get_url, args=[8])
            t4 = threading.Thread(target=self.get_url, args=[8])
            t5 = threading.Thread(target=self.get_url, args=[8])
            t6 = threading.Thread(target=self.get_url, args=[8])
            t7 = threading.Thread(target=self.get_url, args=[8])
            t8 = threading.Thread(target=self.get_url, args=[8])

            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()
            t6.start()
            t7.start()
            t8.start()

            thread_list.append(t1)
            thread_list.append(t2)
            thread_list.append(t3)
            thread_list.append(t4)
            thread_list.append(t5)
            thread_list.append(t6)
            thread_list.append(t7)
            thread_list.append(t8)

            print('Project start at %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            # 让主线程阻塞，等待所有的子线程结束，再继续执行。
            for thread in thread_list:
                thread.join()
        except:

            print('Error: unable to start thread')

if __name__ == '__main__':

    d = Download()

    d.run()
