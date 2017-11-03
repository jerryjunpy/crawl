#!/usr/bin/python
# -*- coding: utf-8 -*-
from download import Download
from orderno import Orderno
import time
import datetime


class Kuaidu:
    def __init__(self):
        self.bash_url = 'http://www.kuaidi.com/index-ajaxselectcourierinfo-'
        self.bash_html = '-.html'
        self.orderno = Orderno()

    def data(self):
        """
        构造url链接
        :return: 实际的快递单信息链接
        """
        print('Begin')
        orderno = self.orderno
        orderno_list = orderno.shipping_orderno()
        print('今天要爬取的采购单数目: %s' % len(orderno_list))
        for i in orderno_list:
            url = self.bash_url + i + self.bash_html
            self.get_text(i, url)

    def get_text(self, shippingorderno, url):
        """
        获取快递单信息
        :param shippingorderno:
        :param url: 快递单链接列表
        :return: 快递单号、详细描述、交易时间
        """
        download = Download()
        response = download.get_url(url, 5)
        if response:
            try:
                j = response.json()
                print("开始获取%s的信息 " % shippingorderno)
            except:
                pass
            else:
                for data in j['data']:
                    track_date = data['time'].strip()
                    description = data['context'].strip()
                    self.save_date(shippingorderno, description, track_date)
            time.sleep(0.8)

    def save_date(self, shippingorderno, description, track_date):
        """
        保存至数据库
        :param shippingorderno:
        :param description:
        :param track_date:
        :return:
        """
        order = self.orderno
        db = order.db
        create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = order.cursor
        data = {
            'shippingorderno': shippingorderno,
            'description': description,
            'create_date': create_date,
            'track_date': track_date,
        }
        table = 'shippingtrackdetail'
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        # 已存在的数据不再存入
        cursor.execute("select * from shippingtrackdetail WHERE shippingorderno='{}' "
                       "and description='{}'".format(shippingorderno, description))
        isExists = cursor.rowcount
        if not isExists:
            try:
                cursor.execute(sql, tuple(data.values()))
                print('%s:%s save successful' % (shippingorderno, description))
                db.commit()
            except:
                print('Failed')
                db.rollback()
        else:
            print('%s:%s 已经存在' % (shippingorderno, description))
