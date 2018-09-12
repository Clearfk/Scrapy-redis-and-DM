# -*- coding: utf-8 -*-

# Scrapy settings for Dongfang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Dongfang'

SPIDER_MODULES = ['Dongfang.spiders']
NEWSPIDER_MODULE = 'Dongfang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Dongfang (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {开启爬取得中间件
#    'Dongfang.middlewares.DongfangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {#开启下载中间件
#    'Dongfang.middlewares.ProxyMiddlewares': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 还有在scrapy_redis包中,有一个pipelines文件,里面的RedisPipeline类可以把爬虫的数据写入redis,\
# 更稳定安全,所以要在settings中启动pipelines的地方启动此pipeline
ITEM_PIPELINES = {
   # 'Dongfang.pipelines.DongfangPipeline': 10,
    'scrapy_redis.pipelines.RedisPipeline':50,#分布式包scrapy_redis中的一个管道类
   'Dongfang.Mongopipelines.Mongopipe':10,
   # 'Dongfang.Mysqlpipeline.MysqlTwistedPipeline': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#配置mongodb数据库
ROBOTSTXT_OBEY = False
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'Dongfang'
MONGODB_DOCNAME = 'good2'

#配置异步mysql数据库链接参数
# 数据库地址
MYSQL_HOST = 'localhost'
# 数据库用户名:
MYSQL_USER = 'root'
#数据库密码
MYSQL_PASSWORD = ''
#数据库端口
MYSQL_PORT = 3306
#数据库名称
MYSQL_DBNAME = 'dongfgoods'
#数据库编码
MYSQL_CHARSET = 'utf8'


#配置分布式数据库redis
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
REDIS_URL = None # 本地的话一般情况可以省去
#要是链接其他主机则要写成如：
# REDIS_URL = 'redis://root:@192.168.0.8:6379'
REDIS_HOST = '127.0.0.1' # 也可以根据情况改成 localhost
REDIS_PORT = 6379

#分布式去重的设置
# 在下载的scrapy_redis包中,有一个scheduler.py文件,里面有一个Scheduler类,是用来调度url,还有一个dupefilter.py文件,\
# 里面有个类是RFPDupeFilter,是用来去重,所以要在settings任意位置文件中添加上它们
#使用scrapy_redis中的调度器，来保证每台主机上爬取的url地址都不一样Scheduler
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

#设置scrapy使用的去重类RFPDupeFilter

DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'