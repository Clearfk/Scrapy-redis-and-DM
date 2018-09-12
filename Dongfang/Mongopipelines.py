import pymongo
from scrapy.conf import settings
class Mongopipe(object):
    #实现插入mongodb数据库至少要实现下面这两个函数__init__(self)和 process_item(self,item,spider)这两个函数
    #构造函数创建mongodb数据库的初始化
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        # biao_name = settings['MONGODB_DOCNAME']
        #创建数据库连接对象
        client = pymongo.MongoClient(host=host,port=port)
        #创建连接的数据库名字
        db = client[db_name]
        self.post = db[settings['MONGODB_DOCNAME']]
    def process_item(self, item, spider):#插入数据必须重写process_item(self,item,spider)函数才可以插入
        good_info = dict(item)#将item转为字典的形式插入mongodb
        self.post.insert(good_info)
        print('**************已经存入mongodb数据库*****************')
        return item


