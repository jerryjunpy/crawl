#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql
import re


class Orderno():
    def __init__(self):
        self.db = pymysql.connect(host='your dress', user='username', password='password', port=3306, db='',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def repleni_orderno(self):
        """
        获取单列表
        :return:
        """
        sql = ""
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
                    sql = ""
                    cursor.execute(sql)
                    isExists = cursor.rowcount
                    if not isExists:
                        repleni_orderno.append(n)
            return repleni_orderno
        except:
            pass

    def shipping_orderno(self):
        """
        获取单列表，并将两个表合并
        :return:
        """
        sql = ""
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
                    sql = ""
                    cursor.execute(sql)
                    isExists = cursor.rowcount
                    if not isExists:
                        orderno.append(n)
            return orderno
        except:
            pass

