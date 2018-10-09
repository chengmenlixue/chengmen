# 微博联系人微博爬取

## 01_scrapy框架创建爬虫

```terminal
# 创建爬虫项目
scrapy startproject weibo_project

# 进入爬虫项目目录
cd weibo_project

# 生成爬取spider文件
scrapy genspider weibo www.weibo.com

```

* 生成文件树（tree /f）

  │  ceshi.py （测试文件）
  │  main.py （启动文件）
  │  scrapy.cfg
  │
  └─weibo_project
      │  items.py 
      │  middlewares.py  (中间件)
      │  pipelines.py
      │  settings.py  （scrapy 设置文件）
      │  __init__.py  
      │
      ├─spiders
      │  │  weibo.py （微博爬虫文件）
      │  │  __init__.py
      │  │
      │  └─__pycache__
      │          weibo.cpython-36.pyc
      │          __init__.cpython-36.pyc
      │
      └─__pycache__
              settings.cpython-36.pyc
              __init__.cpython-36.pyc



##02: 创建初始请求和请求头信息

* 分析
  * 使用手机端微博api不需要携带cookie
  * 移动端微博加密少， 可直接获取数据
* 请求初始主页地址 ， 获取基本信息

weibo.py

```python
# -*- coding: utf-8 -*-
import scrapy
import json

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']
    id = input('请输入要查询的微博ID:')
    start_urls = [f'https://m.weibo.cn/api/container/getIndex?type=uid&value={id}']

    # 用户设置 优先级高于默认设置
    custom_settings = {
        'COOKIE_ENABLED':False,
        'DEFAULT_REQUEST_HEADERS' :{
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        }
    }


    def parse(self, response):
        data = response.body.decode('unicode_escape') # unicode_excape转中文
        print(data)
        content = json.loads(data).get('data')
        print(content)
        profile_image_url = content.get('userInfo').get('profile_image_url')
        description = content.get('userInfo').get('description')
        profile_url = content.get('userInfo').get('profile_url')
        verified = content.get('userInfo').get('verified')
        guanzhu = content.get('userInfo').get('follow_count')
        name = content.get('userInfo').get('screen_name')
        fensi = content.get('userInfo').get('followers_count')
        gender = content.get('userInfo').get('gender')
        urank = content.get('userInfo').get('urank')
        print(
            "微博昵称：" + name + "\n" + "微博主页地址：" + profile_url + "\n" + "微博头像地址：" + profile_image_url + "\n" + "是否认证：" + str(
                verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" + "粉丝数：" + str(
                fensi) + "\n" + "性别：" + gender + "\n" + "微博等级：" + str(urank) + "\n")

```





## 存储：存储到mysql

* 生成两张关联表：一张主页表， 一张内容表







## urllib爬取微博

```python 
# -*- coding: utf-8 -*-

import urllib.request
import json

#定义要爬取的微博大V的微博ID
id='3985030785'

#设置代理IP
proxy_addr="223.72.91.104:8080"

#定义页面打开函数
def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler({'http':proxy_addr})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data

#获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data.get('tab_type')=='weibo'):
            containerid=data.get('containerid')
    return containerid

#获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    profile_image_url=content.get('userInfo').get('profile_image_url')
    description=content.get('userInfo').get('description')
    profile_url=content.get('userInfo').get('profile_url')
    verified=content.get('userInfo').get('verified')
    guanzhu=content.get('userInfo').get('follow_count')
    name=content.get('userInfo').get('screen_name')
    fensi=content.get('userInfo').get('followers_count')
    gender=content.get('userInfo').get('gender')
    urank=content.get('userInfo').get('urank')
    print("微博昵称："+name+"\n"+"微博主页地址："+profile_url+"\n"+"微博头像地址："+profile_image_url+"\n"+"是否认证："+str(verified)+"\n"+"微博说明："+description+"\n"+"关注人数："+str(guanzhu)+"\n"+"粉丝数："+str(fensi)+"\n"+"性别："+gender+"\n"+"微博等级："+str(urank)+"\n")


#获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id,file):
    i=1
    while True:
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
            cards=content.get('cards')
            if(len(cards)>0):
                for j in range(len(cards)):
                    print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    card_type=cards[j].get('card_type')
                    if(card_type==9):
                        mblog=cards[j].get('mblog')
                        attitudes_count=mblog.get('attitudes_count')
                        comments_count=mblog.get('comments_count')
                        created_at=mblog.get('created_at')
                        reposts_count=mblog.get('reposts_count')
                        scheme=cards[j].get('scheme')
                        text=mblog.get('text')
                        with open(file,'a',encoding='utf-8') as fh:
                            fh.write("----第"+str(i)+"页，第"+str(j)+"条微博----"+"\n")
                            fh.write("微博地址："+str(scheme)+"\n"+"发布时间："+str(created_at)+"\n"+"微博内容："+text+"\n"+"点赞数："+str(attitudes_count)+"\n"+"评论数："+str(comments_count)+"\n"+"转发数："+str(reposts_count)+"\n")
                i+=1
            else:
                break
        except Exception as e:
            print(e)
            pass  

if __name__=="__main__":
    file=id+".txt"
    get_userInfo(id)
    get_weibo(id,file)
```























## 参考资料：

_01: https://www.cnblogs.com/goforwards/p/8978002.html

_02:https://blog.csdn.net/a349458532/article/details/51690892(编码问题解决)

_03:https://blog.csdn.net/sunhaobo1996/article/details/72730895(cookie分析获取)

_04:https://blog.csdn.net/d1240673769/article/details/74278547(简单urllib抓取微博)

_05:https://blog.csdn.net/qq_42156420/article/details/80746774（scrapy框架简介）

_06:https://blog.csdn.net/qq_29883591/article/details/78177279（python中input的使用）