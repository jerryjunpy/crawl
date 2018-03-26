#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql
import redis
import datetime
import time


def save_yanwen():

    redis_client = redis.Redis(host='....', port=6379)

    while True:

        yuntrack = redis_client.lpop('shuefeng_item')

        if yuntrack:
           
           j = (str(yuntrack, encoding="utf-8"))
            
            data = eval(j)

            logistics_name = 'sfexpress'
            
            tracking_number = data['nu']
            
            status = data['originCountryData']['stausDataNum']
            
            if status == 4 or status == 5:
                # 已签收  取第倒数一个为上网时间

                for a in data['originCountryData']['trackinfo'][-2: -1]:
                    info_date = a['Date'].strip()
                    info_content = a['StatusDescription'].strip()
                    save_date(tracking_number, info_content, info_date, logistics_name, tracking_status='1')

                for b in data['originCountryData']['trackinfo'][:1]:  # 取第一条数据为妥投
                    info_date = b['Date'].strip()
                    info_content = b['StatusDescription'].strip()
                    save_date(tracking_number, info_content, info_date, logistics_name, tracking_status='2')

                for c in data['originCountryData']['trackinfo'][1:-2]:  # 中间的数据，交运数据已存可以去重复

                    info_date = c['Date'].strip()
                    info_content = c['StatusDescription'].strip()
                    save_date(tracking_number, info_content, info_date, logistics_name)

            elif status != 4 or status != 5:  # 未签收  取第一个为上网时间

                for a in data['originCountryData']['trackinfo'][-2:-1]:
                    info_date = a['Date'].strip()
                    info_content = a['StatusDescription'].strip()
                    save_date(tracking_number, info_content, info_date, logistics_name, tracking_status='1')

                for c in data['originCountryData']['trackinfo'][:-2]:  # 中间的数据，交运数据已存可以去重复

                    info_date = c['Date'].strip()
                    info_content = c['StatusDescription'].strip()
                    save_date(tracking_number, info_content, info_date, logistics_name)


def save_date(tracking_number, info_content, info_date, logistics_name, tracking_status=''):
    """
    写入数据
    :param tracking_number:
    :param description:
    :param info_data:
    :return:
    """
    db = pymysql.connect(host='', user='', password='', port=3306, db='',
                         charset='utf8')
    cursor = db.cursor()
    db_1 = pymysql.connect(host='', user='', password='', port=3306, db='',
                           charset='utf8')
    # 已存在的数据不再去查询存入

    cursor.execute("select * from logistics_info WHERE tracking_number=\"{}\" "
                   "and info_content=\"{}\" and info_date=\"{}\"".format(tracking_number, info_content, info_date))

    isExists = cursor.rowcount

    if not isExists:  # 将数据库中没有的数据保存进去

        cursor_1 = db_1.cursor()

        sql_1 = "SELECT customerorderno pmsorder, ebayorderid salechannelorderid, shippingforwardermethod, salechannel " \
                "FROM customerorder where shippingorderno ='{}';".format(tracking_number)

        cursor_1.execute(sql_1)
        result = cursor_1.fetchone()
        
        try:
            pms_order_id = result[0]
            sale_channel_order_id = result[1]
            logistics_method = result[2]
            sale_channel = result[3]

        except TypeError as e:
            
            print(e)

        else:
            creation_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if tracking_status:
                data = {
                    'tracking_number': tracking_number,
                    'info_content': info_content,
                    'creation_date': creation_date,
                    'info_date': info_date,
                    'logistics_name': logistics_name,
                    'tracking_status': tracking_status,
                    'pms_order_id': pms_order_id,
                    'sale_channel_order_id': sale_channel_order_id,
                    'logistics_method': logistics_method,
                    'sale_channel': sale_channel,

                }
            else:
                data = {
                    'tracking_number': tracking_number,
                    'info_content': info_content,
                    'creation_date': creation_date,
                    'info_date': info_date,
                    'logistics_name': logistics_name,
                    'pms_order_id': pms_order_id,
                    'sale_channel_order_id': sale_channel_order_id,
                    'logistics_method': logistics_method,
                    'sale_channel': sale_channel,
                }

            table = 'logistics_info'
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)

            try:

                cursor.execute(sql, tuple(data.values()))
                print('%s:%s save successful' % (tracking_number, info_content))

                db.commit()


            except:

                print('Failed')
                db.rollback()

if __name__ == '__main__':
    save_yanwen()

