# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors

class XbiqugePipeline(object):
    #定义类初始化动作，包括连接数据库novels及建表
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'password',
            'database':'novels',
            'charset':'utf8mb4'   #使用utf8mb4字符集可避免emoji表情符号无法存入数据表的错误，这是因为mysql的utf8只支持3个字节的存储，而一般字符是3个字节，但是emoji表情符号是4字节。

        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None
        self.name_novel = "xiaoyaoxss"   #此处为小说的英文或拼音名，此名也是小说存储表文件名。
        self.url_firstchapter = "https://www.booktxt.net/4_4579/1672967.html"  #此处为小说的第一章节链接地址。
        self.name_txt = "逍遥小书生"   #此处为小说的中文名称，输出文件以此命名。


    #建表
    def createtable(self):
        self.cursor.execute("drop table if exists "+ self.name_novel)  
        self.cursor.execute("create table " + self.name_novel + " (id int unsigned auto_increment not null primary key, url varchar(50) not null, preview_page varchar(50), next_page varchar(50), content TEXT not null) charset=utf8mb4")
        return

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['url'], item['preview_page'], item['next_page'], item['content']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into """ + self.name_novel + """(id, url, preview_page, next_page, content) values(null, %s, %s, %s, %s)
                """
            return self._sql
        return self._sql


    #从数据库取小说章节内容写入txt文件
    def content2txt(self):
        self.cursor.execute("select count(*) from " + self.name_novel)
        record_num = self.cursor.fetchall()[0][0]
        print(record_num)
        counts=record_num
        url_c = "\""+self.url_firstchapter+"\""
        start_time=time.time()  #获取提取小说内容程序运行的起始时间
        f = open(self.name_txt+".txt", mode='w', encoding='utf-8')   #写方式打开小说名称加txt组成的文件
        for i in range(counts):
            sql_c = "select content from " + self.name_novel + " where url=" + url_c  #组合获取小说章节内容的sql命令。此处需要修改数据库文件名称
            self.cursor.execute(sql_c)
            record_content_c2a0=self.cursor.fetchall()[0][0]  #获取小说章节内容
            record_content=record_content_c2a0.replace(u'\xa0', '\n')  #消除特殊字符\xc2\xa0
            f.write('\n')
            f.write(record_content + '\n')
            f.write('\n\n')
            sql_n = "select next_page from " + self.name_novel + " where url=" + url_c   #组合获取下一章链接的sql命令。此处需要修改数据库>文件名称
            self.cursor.execute(sql_n)
            url_c = "\"" + self.cursor.fetchall()[0][0] + "\""  #下一章链接地址赋值给url_c，准备下一次循环。
        f.close()
        print(time.time()-start_time)
        print(self.name_txt + ".txt" + " 文件已生成！")
        return
