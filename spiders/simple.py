import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        # next_page = response.css('li.next a::attr(href)').extract_first()
        next_page = response.xpath('.//li[@class="next"]/a/@href').extract_first()
        next_page = response.urljoin(next_page)
        print('%%%%%%%%%%%%%', next_page)

        if next_page:
            # yield response.follow(next_page, callback=self.parse)

            yield scrapy.Request(next_page, callback=self.parse)