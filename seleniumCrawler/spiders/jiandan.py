# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from seleniumCrawler.items import MeizituItem
from bs4 import BeautifulSoup
from scrapy.http import Request


class JianDanSpider(RedisSpider):
    name = 'jiandan'
    redis_key = 'jiandan:start_urls'

    # 请求头
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3013.3 Safari/537.36'
    }

    rules = (
        Rule(LinkExtractor(allow='page-\d+\S+', ), 'parse', follow=True, ),
    )

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html.parser")
        item = MeizituItem()
        item['tags'] = '煎蛋'
        item['name'] = '美女'
        item['image_urls'] = []
        sites = soup.findAll("a", {'class': 'view_img_link'})
        # urls =response.xpath('//div[@class="text"]/p/img/@src').extract()
        for site in sites:
            image_url = site.get('href')
            if not image_url.startswith('http'):
                image_url = 'http:' + image_url
            if image_url.endswith('gif'):
                pass
            else:
                item['image_urls'].append(image_url)
        yield item
        pre_page = soup.find('a', {"class": 'next-comment-page'})
        if pre_page == None :
            print("No More Page")
            return
        pre_page_link = pre_page.get("href")
        if pre_page_link:
            # the last element
            pre_page_url = "http://" + pre_page_link.split("//")[-1]
            yield Request(pre_page_url, callback=self.parse)
        else:
            print("No More Page")
