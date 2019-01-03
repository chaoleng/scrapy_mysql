# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


def dbHandle():
    conn = pymysql.connect(
        host='localhost',
        user='douban',
        passwd='douban',
        charset='utf8',
        use_unicode=False
    )
    return conn



class DoubanPipeline(object):

 def process_item(self, item, spider):
    dbObject = dbHandle()
    cursor = dbObject.cursor()
    sql = "replace into douban_top.douban(serial_number,movie_name,introduce,star,evaluate,describ) values(%s,%s,%s,%s,%s,%s)"
    try:
         cursor.execute(sql,(item['serial_number'],item['movie_name'],item['introduce'],item['star'],item['evaluate'],item['describ']))
         dbObject.commit()
    except Exception as e:
         print (e)
         dbObject.rollback()
    return item
    


# def from_settings(cls, settings):
#     '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
#        2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
#        3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
#     #读取settings中配置的数据库参数
#     dbparams = dict(
#         host=settings['MYSQL_HOST'],  
#         db=settings['MYSQL_DBNAME'],
#         user=settings['MYSQL_USER'],
#         passwd=settings['MYSQL_PASSWD'],
#         charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
#         cursorclass=pymysql.cursors.DictCursor,
#         use_unicode=False,
#     )
#     dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
#     return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

# # pipeline默认调用
# def process_item(self, item, spider):
#     query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
#     query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
#     return item

# # 写入数据库中
# # SQL语句在这里
# def _conditional_insert(self, tx, item):
#     sql = "insert into ty_work(serial_number,movie_name,introduce,star,evaluate,describe) values(%s,%s,%s,%s,%s,%s,%s,%s)"
#     params = (item['author'], item['title'], item['url'], item['pubday'],item['comments'],item['likes'],item['rewards'],item['reads'])
#     tx.execute(sql, params)

# # 错误处理方法
# def _handle_error(self, failue, item, spider):
#     print (failue)

