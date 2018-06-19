#  -*- coding: cp1251 -*-                                                                                             #
# Python 3.x.x

# запускать так: (scrapy runspider up_work_title.py -o result.json)
# запускать так: (scrapy crawl up_py -o result.json) # или по имени паука

# с парамтерами командной строки USER_AGENT:
# scrapy shell "https://www.upwork.com/o/jobs/browse/skill/python" -s USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'

import scrapy




class UpWorkSpider(scrapy.Spider):
    name = 'up_py'
    # allowed_domains = ['upwork.com']
    start_urls = ['https://www.upwork.com/o/jobs/browse/skill/python']


    def parse(self, response):
        # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'} # define in settings.py

        for title in response.xpath('.//section[@class="job-tile"]'):
            yield {
                'name_project': title.xpath('normalize-space(div/div/h4/a/text())').extract_first(),
                'url_to_project': response.urljoin(title.xpath('div/div/h4/a/@href').extract_first()),
                'price': title.xpath('normalize-space(div/div/small/span[@class="js-budget"]/span/text())').extract_first(),
                'level': title.xpath('normalize-space(div/div/small/span[@class="js-contractor-tier"]/text())').extract_first(),
            }


        # next_page = response.xpath('.//link[@rel="next"]/@href').extract_first()
        next_page = response.xpath('.//li[@class="next"]/a/@href').extract_first()
        next_page = response.urljoin(next_page)
        print('^^^^^^^^^^^^^^^^', next_page)

        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)


