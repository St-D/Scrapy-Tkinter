#  -*- coding: cp1251 -*-                                                                                             #
# Python 3.x.x

# запускать так:
# cd D:\Project\Py\00001\upWork\scrap_up_work\up_w>
# (scrapy crawl tst) # или по имени паука

# с парамтерами командной строки USER_AGENT:
# scrapy shell "https://www.upwork.com/o/jobs/browse/skill/python" -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'

import scrapy
from scrapy.loader import ItemLoader
from up_work_spider.items import ScrapTstLoader

from scrapy.loader.processors import TakeFirst, MapCompose, Join

import time


def time_now():
    """ Return Current date """
    t2 = time.time()
    time_tup = time.localtime(t2)
    return time.strftime("%d.%m.%Y", time_tup)


class UpWorkSpider(scrapy.Spider):
    name = 'tst'
    # allowed_domains = ['https://www.upwork.com']
    start_urls = ['https://www.upwork.com/o/jobs/browse/skill/python']

    # handle_httpstatus_list = [301, 302]

    def parse(self, response):
        for title in response.xpath('.//section[@class="job-tile"]'):
            l = ScrapTstLoader(selector=title)
            l.add_xpath('name_project', 'div/div/h4/a/text()')
            l.add_xpath('url_to_project', 'div/div/h4/a/@href')
            l.add_xpath('price', 'div/div/small/span[@class="js-budget"]/span/text()')
            l.add_xpath('level', 'div/div/small/span[@class="js-contractor-tier"]/text()')
            l.add_value('crawl_date', time_now())
            l.add_value('show_status', True)
            yield l.load_item()

        next_page = response.xpath('.//li[@class="next"]/a/@href').extract_first()
        next_page = response.urljoin(next_page)
        next_page = None
        print('^^^^^^NEXT PAGE^^^^^^^^^^', next_page)

        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)



