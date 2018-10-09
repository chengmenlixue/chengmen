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

    # 查看用户信息
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

        # 下载用户所有微博

