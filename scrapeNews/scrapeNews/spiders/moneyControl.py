# -*- coding: utf-8 -*-
import scrapy
from scrapeNews.items import ScrapenewsItem
import logging
loggerError = logging.getLogger("scrapeNewsError")

class MoneycontrolSpider(scrapy.Spider):
    name = 'moneyControl'
    allowed_domains = ['moneycontrol.com']

    def __init__(self, pages=10, *args, **kwargs):
        super(MoneycontrolSpider, self).__init__(*args, **kwargs)
        for count in range(1 , int(pages)+1):
            self.start_urls.append('http://www.moneycontrol.com/news/business/page-'+ str(count))

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        newsContainer = response.xpath("//ul[@id='cagetory']/li[@class='clearfix']")
        for newsBox in newsContainer:
            item = ScrapenewsItem()  # Scraper Items
            item['image'] = self.getPageImage(newsBox)
            item['title'] = self.getPageTitle(newsBox)
            item['content'] = self.getPageContent(newsBox)
            item['newsDate'] = self.getPageDate(newsBox)
            item['link'] = self.getPageLink(newsBox)
            item['source'] = 108
            if item['image'] is not 'Error' or item['title'] is not 'Error' or item['content'] is not 'Error' or item['link'] is not 'Error' or item['newsDate'] is not 'Error':
                yield item

    def getPageContent(self, newsBox):
        data = newsBox.xpath('p/text()').extract_first()
        if (data is None):
            loggerError.error(response.url)
            data = 'Error'
        return data

    def getPageTitle(self, newsBox):
        data = newsBox.xpath('h2/a/text()').extract_first()
        if (data is None):
            loggerError.error(response.url)
            data = 'Error'
        return data

    def getPageLink(self, newsBox):
        data = newsBox.xpath('a/@href').extract_first()
        if (data is None):
            loggerError.error(response)
            data = 'Error'
        return data

    def getPageImage(self, newsBox):
        data = newsBox.xpath('a/img/@src').extract_first()
        if (data is None):
            loggerError.error(response.url)
            data = 'Error'
        return data

    def getPageDate(self, newsBox):
        data = newsBox.xpath('span/text()').extract_first()
        if (data is None):
            loggerError.error(response.url)
            data = 'Error'
        return data
