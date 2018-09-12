# -*- coding: utf-8 -*-
import scrapy
# import time
#改写成分布式
# 引入分布式包，这是scrapy改写为分布式的前提
from scrapy_redis.spiders import RedisSpider
from ..items import DongfangItem
# class DongfgoodSpider(scrapy.Spider):#将原来的父类写成继承为分布式的父类RedisSpider如下
class DongfgoodSpider(RedisSpider):
    name = 'Dongfgood'
    allowed_domains = ['http://www.ocj.com.cn']
    # start_urls = ['http://www.ocj.com.cn/']
    #注释掉start_url,设置成分布式的
    redis_key = 'Dongfgood:start_urls'#一般为爬虫名：start_urls
    #分布式项目的起始点url为http://www.ocj.com.cn/
    #在redis客户端redis-cli.exe下执行：lpush Dongfgood:start_urls http://www.ocj.com.cn/把起始url压入第一个url队列便可
    #下面的爬取代码分布式和原来是一样的
    #headers放在这里的时候相当于放在setting中，这此时setting中的headers失效了。覆盖掉了
    headers={
        "User - Agent": "Mozilla / 5.0(Linux;Android6.0;Nexus5Build / MRA58N) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.79MobileSafari / 537.36"
        # # "Referer": "http: // www.ocj.com.cn",
        # "Cookie": "returnUrlBefore = http % 3A % 2F % 2Fwww.ocj.com.cn % 2Fdetail % 2F15222122;cookieID = 6406477566227517000;rcust_id = 7803CB75 - FFC8 - 4661 - B8E7 - 3C5A6E8AE898;Hm_lvt_42074410ff8ee03053c061cd4fe58d53 = 1531139730;c_code = 2000;sel_region_cd = 2000;substation_code = 100;district_code = 1000;area_lgroup = 10;area_mgroup = 001;_ga = GA1.3.1699733175.1527423203;JSESSIONID = L3bLbDWBHpym26FJ2ySrd0Xy0JBqdvfLRKt86h2MKJqC9yTMhKHM!-1969589725!-978629879;ocj_jplayer_tabindex = 0;SCART_ID = 807098817852;Hm_lpvt_42074410ff8ee03053c061cd4fe58d53 = 1531139730;_gid = GA1.3.573254848.1531139733;_gat = 1",
        # "Connection": "keep - alive"
    }

    """知识扩充：

    # 1.可以重写scrapy中的start_requests()方法使其的第一次访问网页时就模拟浏览器带上了headers，或带上表单的post请求以下举例说明：
    def start_requests(self):
        start_url  = '第一次发起的请求url'
        headers = {"User - Agent":"xx"}  #设置headers头参数元组的格式
        cookies = {}#设置cookies参数
        # 利用yield提交请求，带上headers等参数，将返回的结果交给类内部方法parse()来处理
        yield scrapy.Request(url=start_url,headers=headers,callback=self.parse,cookies=cookies)
    #2.重写start_requests()方法，带上表单提交信息
    # scrapy.Request函数还有一个meta参数,值为字典格式,作用是携带数据在指定的回调函数中使用,使用方法:response.meta['键']
    #携带data数据进行post请求提交利用表单提交方法scrapy.FormRequest()进行登录表单请求提交
    def start_requests(self):
        login_url = '要登录或提交表单的url'
        data = {"username":"", "password":"",}#要提交的信息，如账号密码等
        #提交表单数据,将返回的结果交给类中的after_login()方法进行处理，如验证码的处理等
        yield scrapy.FormRequest(url=login_url,formdata=data,callback=self.after_login)
    #对登录后返回结果的处理可以使用以下方法
    # scrapy.FormRequest.from_response方法可以从响应中自动提取表单POST地址, 
    # 例如处理登录, 需要先返回登录页面, 再填充表单, 然后提交
        # 自动提取表单post地址
        yield scrapy.FormRequest.from_response(response,
            headers=self.headers,
            formdata=data,
            callback=self.after_login,
        )
    # 实现after_login()方法
    def after_login(self,response):
        pass

    3.设置代理与随机选择请求头
    通过下载器中间件来设置请求.
    免费代理:
    request.meta['proxy'] = 'https://' + '代理IP'
    收费代理: 需要先将账号密码base64编码, 再设置给request, 然后设置request.meta['proxy']:
    auth = base64.b64encode({'帐号': '密码'})  # base64需要导入
    request.headers['Proxy-Authorization'] = 'Basic ' + auth
    request.meta['proxy'] = 'https://' + '代理IP'
    举例：
    # coding:utf8    
    from settings import USER_AGENS, PROXIES
    import random
    import base64
    # 随机更换浏览器身份中间件，在scrapy框架的中间件中写
    class RandomUserAgent(object):
        def process_request(self, request, spider):
            user_agent = random.choice(USER_AGENS)
            request.headers.setdefault('User-Agent', user_agent)

    # 随机更换代理ip中间件，在框架的中间件中写
    class RandomProxy(object):
        def process_request(self, request, spider):
            proxy = random.choice(PROXIES)  # 随机选出一个代理
            if proxy.get('auth') is None:  # 免费代理
                request.meta['proxy'] = 'https://' + proxy['host']
            else:  # 收费代理
                auth = base64.b64encode(proxy['auth'])
                request.headers['Proxy-Authorization'] = 'Basic ' + auth
                request.meta['proxy'] = 'https://' + proxy['host']

"""

    def parse(self, response):#先是首页的获取,这个函数获取完首页的所有链接并进行分类提交给不同的函数进行处理
        #1.分类商品列表连接的获取
        #2.观察首页只要得到div的class为hIndexLeftNavInfoListContentBoxSmallButton的节点下的a标签的href属性值

        #建立选择器对首页元素进行选区
        sel = scrapy.Selector(response)
        #(2)对数据进行提取
        #/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[1]/a

        #extract()将选择器的内容转化为列表
        catergory_list = sel.xpath('//div[@class="hIndexLeftNavInfoListContentBoxSmallButton"]/a/@href').extract()
        # print(catergory_list)

        #判断连接是否缺损，即是否存在http://www.ocj.com.cn,利用for循环和if语句进行判断和修正

        for url in catergory_list:
            if "http://www.ocj.com.cn" not in url:
                url = "http://www.ocj.com.cn" + url
            #链接修正后，把链接交给下一个处理机制进行获取详细页面链接
            yield scrapy.Request(url,headers=self.headers,callback=self.parse_category,dont_filter = True)#将链接提交给本类中的parse_category函数进行处理,设置dont_filter= True是为了防止爬取到的url与allowed_domains出现问题而无法发起请求
            #以上完成了分类商品列表链接的获取
            # print('分类商品的分类链接已经提交出去************************************')

        #接下来是首页的商品详细页面链接的获取
        #观察首页我们知道获取div的class为hItemShowImg的节点下的a标签的href链接
        #(1)
        good_info_list = sel.xpath('//div[@class="hItemShowImg"]/a/@href').extract()
        #(2)判断连接是否缺损，然后进行修正，并提交给另一个函数进行处理
        print(good_info_list)
        for url in good_info_list:
            if "http://www.ocj.com.cn" not in url:
                url = "http://www.ocj.com.cn"+url
            yield scrapy.Request(url,callback=self.parse_good_info,headers=self.headers,dont_filter=True)
            # print('***********************************' + url)
            # print(url)
            # time.sleep(2)
    #创建两个处理连接的函数处理parse()函数提交来的链接
    #分类商品的处理方法

    def parse_category(self,response):
        sel = scrapy.Selector(response)
        base_url = "http://www.ocj.com.cn"
        # print(response.url)
        # print('到达每个分类的页面************************************')
        #主要分为两步
        #1 获取详细页面的链接
        #http://www.ocj.com.cn/catalog/3521/251?promotions=0&tvname=0&seq_cate_num=251&showType=datu&search=orderdesc&brandCode=&priceRange=&prop_valie_code=&currPageNo=1&seq_shop_num=3521&isMoreSelect=&myzj=0
        #上一条连接是大图模式
        #http://www.ocj.com.cn/catalog/3521/251?promotions=0&tvname=0&seq_cate_num=251&showType=liebiao&search=orderdesc&brandCode=&priceRange=&prop_valie_code=&currPageNo=1&seq_shop_num=3521&isMoreSelect=&myzj=0
        #这条连接是列表形式的链接
        good_info_url_list = sel.xpath('//p[@class="title"]/a/@href').extract()
        # print(good_info_url_list)
        #获取商品详细页面的链接，并把连接交给详细商品页面的处理函数进行处理

        for url in good_info_url_list:
            if base_url not in url:
                url = base_url+url
            yield scrapy.Request(url,callback=self.parse_good_info,headers=self.headers,dont_filter=True)#将分类商品的每个商品的详细页面的链接提交给详细信息获取函数获取
            # print('每个分类的每个商品的详细页面的url已经提交出去************************************' )
        #2 分类机制的处理
        #对页面的下一页的处理机制进行分析，即判断是否是动态加载的分页机制
        #通过分析我们知道东方购物网的分页机制是唯一的在一个class="page-next"的a连接中
        Nextpage_url = sel.xpath('//a[@class="page-next"]/@href').extract()
        #对连接进行修正
        #是否存在下一页进行判断就是是否已经翻完页

        if Nextpage_url:
            if Nextpage_url[0] == 'javascript:;':#因为Nextpage_url已经转为列表了，当他等于'javascript:;'的时候就是没有下一页的时候
                print(u'数据提取完成！')
            else:
                #存在下一页继续爬取
                #将下一页的链接提交给自己函数再处理一次
                yield scrapy.Request(base_url+Nextpage_url[0],callback=self.parse_category,dont_filter=True)
        else:
            print("页数抓取完成！！")

    #所有的详细商品的共同处理方法
    def parse_good_info(self,response):
        try:
            #是否可以把所有的链接都来到这里处理
            # print("*********到达页面的详细信息的抓取******************************")
            sel = scrapy.Selector(response)
            item = DongfangItem()
            print('*******************************************商品详细页面的连接为'+response.url)
            title = sel.xpath('//div[@class="pv_shop_detail_title"]/h1/text()').extract()
            #有一些商品的title的xpath路径不一样为sel.xpath(// *[ @ id = "containerContent"] / div[1] / div[1] / h1 / text()).extract()
            #故在这里对title做一个判断是否为空值，如果为空值这利用第二种的xpath方法爬取
            if title == None :
                title = sel.xpath('// *[ @ id = "containerContent"] / div[1] / div[1] / h1 / text()').extract()
            else:
                pass
            #//*[@id="containerContent"]/div[1]/div[2]/div[2]/div/dl[2]/dd/span
            # // *[ @ id = "containerContent"] / div[1] / div[2] / div[2] / div / dl[2] / dd / span
            price = sel.xpath('//*[@id="containerContent"]/div[1]/div[2]/div[2]/div/dl[2]/dd/span/text()').extract()#价格转为数组后去掉价格中的逗号
            #id = sel.xpath('//div[@class="info_box"]/div[@class="@no clear_float"]/div[@class="val"]/text()').extract()
            id = sel.xpath('//div[@class="info_box"]/dl[1]/dd[1]/text()').extract()
            score = sel.xpath('string(//p[@class="score"][1])').extract()#string()可以获取当前标签的所以文本信息
            place = sel.xpath('//div[@class="parameter"]/div[3]/text()').extract()
            comment = sel.xpath('//*[@id="detail_bl_tt"]/ul/li[3]/span/label/em/text()').extract()
            # print(id[0])
            # print(title[0].strip())
            # print(price[0].strip(u'￥'))
            # print(place[0])
            # print(score[0].strip())
            #将数据赋值到Item中，并进行数据清洗
            item['good_url'] =response.url
            item['good_title'] = title[0]
            item['good_price'] = int(price[0].strip(u'￥').replace(',',''))#strip()方法取出数据，取出两端的￥符号,加u防止编码错误,并强制转为整型，方便数据分析
            item['good_id'] = id[0]
            item['good_score'] = score[0].strip()#strip()取出数据取出两端的空格，数据清洗的重要函数
            item['good_place'] = place[0]
            item['good_com'] = int(comment[0].strip(u'["("|")"]'))#去掉评论数两边的括号符号()，并强制转为整型，方便数据分析
            # 获取完数据后返回给管道处理，就是返回Item
            # print(item['good_title'])
            yield item
            # print(response.url)
        except:
            print('连接为  '+response.url+'   的商品信息查找失败！！')
    #         yield scrapy.Request(response.url, callback=self.parse_good_info2, headers=self.headers,dont_filter=True)
    # #如果第一个方法找不到信息可以把请求再发送一次调用第二个方法来解析
    # def parse_good_info2(self,response):
    #     try:
    #         #是否可以把所有的链接都来到这里处理
    #         # print("*********到达页面的详细信息的抓取******************************")
    #         sel = scrapy.Selector(response)
    #         item = DongfangItem()
    #         print('*******************************************商品详细页面的url'+response.url)
    #         title = sel.xpath('//div[@class="pv_shop_detail_title"]/h1/text()').extract()
    #         #商品价格xpath路径不同之处
    #         #//*[@id="containerContent"]/div[1]/div[2]/div[2]/div/dl[2]/dd/span
    #         # // *[ @ id = "containerContent"] / div[1] / div[2] / div[2] / div / dl[2] / dd / span
    #         # // *[ @ id = "containerContent"] / div[1] / div[2] / div[2] / div / dl[2] / dd / span
    #         # // *[ @ id = "containerContent"] / div[1] / div[2] / div[2] / div / dl[2] / dd / span
    #
    #         price = sel.xpath('//*[@id="containerContent"]/div[1]/div[2]/div[2]/div/dl[3]/dd/span/text()').extract()
    #         #id = sel.xpath('//div[@class="info_box"]/div[@class="@no clear_float"]/div[@class="val"]/text()').extract()
    #         id = sel.xpath('//div[@class="info_box"]/dl[1]/dd[1]/text()').extract()
    #         score = sel.xpath('string(//p[@class="score"][1])').extract()#string()可以获取当前标签的所以文本信息
    #         place = sel.xpath('//div[@class="parameter"]/div[3]/text()').extract()
    #         # print(id[0])
    #         # print(title[0].strip())
    #         # print(price[0].strip(u'￥'))
    #         # print(place[0])
    #         # print(score[0].strip())
    #         #将数据赋值到Item中，并进行数据清洗
    #         item['good_url'] = response.url
    #         item['good_title'] = title[0]
    #         item['good_price'] = price[0].strip(u'￥')#strip()方法取出数据，取出两端的￥符号,加u防止编码错误
    #         item['good_id'] = id[0]
    #         item['good_score'] = score[0].strip()#strip()取出数据取出两端的空格，数据清洗的重要函数
    #         item['good_place'] = place[0]
    #         # 获取完数据后返回给管道处理，就是返回Item
    #         # print(item['good_title'])
    #         yield item
    #         # print(response.url)
    #     except:
    #         print('采用第二个方法信息查找失败！！')
    #         # yield scrapy.Request(response.url, callback=self.parse_good_info, dont_filter=True)


