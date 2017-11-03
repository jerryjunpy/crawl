#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql
import re


class Orderno():
    def __init__(self):
        self.db = pymysql.connect(host='192.168.1.242', user='nijun', password='nijun', port=3306, db='pms',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def repleni_orderno(self):
        """
        获取shippingorderno单列表
        :return:
        """
        sql = "select shippingorderno from purchasetask where stockinstatus != 'All Stock In' " \
              "and shippingorderno != '' and (purchasetask_process_step in ('Start','Under Supervisor Confirmation'," \
              "'Under Confirmation','Confirmed','Awaiting Products','Check In Products','Partial Check In') or " \
              "purchasetask_process_step is null) and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= purchase_date" \
              " ORDER BY purchase_date"
        cursor = self.cursor
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            ls = []
            for i in range(len(results)):
                if results[i][0]:
                    ls.append(results[i][0])
            replen = []
            for row in ls:
                result = re.findall('[0-9]{8,}', row)
                if result:
                    replen.append(result)
            # 检测已完成的订单不再去查询
            repleni_orderno = []
            for m in replen:
                for n in m:
                    sql = "SELECT * from shippingtrackdetail where shippingorderno='{}' " \
                          "and description LIKE '%{}%'".format(n, '签收')
                    cursor.execute(sql)
                    isExists = cursor.rowcount
                    if not isExists:
                        repleni_orderno.append(n)
            return repleni_orderno
        except:
            pass

    def shipping_orderno(self):
        """
        获取replenishmentorderno单列表，并将两个表合并
        :return:
        """
        sql = "select replenishmentorderno from purchasetask where stockinstatus != 'All Stock In' " \
              "and shippingorderno != '' and (purchasetask_process_step in ('Start','Under Supervisor Confirmation'," \
              "'Under Confirmation','Confirmed','Awaiting Products','Check In Products','Partial Check In') or " \
              "purchasetask_process_step is null) and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= purchase_date " \
              "ORDER BY purchase_date;"
        cursor = self.cursor
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            ls = []
            for i in range(len(results)):
                if results[i][0]:
                    ls.append(results[i][0])
            replen = []
            for row in ls:
                result = re.findall('[0-9]{8,}', row)
                if result:
                    replen.append(result)
            # 检测已完成的订单不再去查询
            orderno = self.repleni_orderno()
            for m in replen:
                for n in m:
                    sql = "SELECT * from shippingtrackdetail where shippingorderno='{}' " \
                          "and description LIKE '%{}%'".format(n, '签收')
                    cursor.execute(sql)
                    isExists = cursor.rowcount
                    if not isExists:
                        orderno.append(n)
            return orderno
        except:
            pass

