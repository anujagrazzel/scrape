import scrapy
from zee.items import ZeeItem

class zeespider(scrapy.Spider):
    name = "zee"
    start_urls = ['http://zeenews.india.com/india',]

    #Scraping the main page for article links
    def parse(self, response):
        articles = response.xpath('//section[contains(@class, "maincontent")]//div[contains(@class, "section-article")]') #extracts HTML from the start_url
        for article in articles:
            x = article.xpath('.//h3/a[2]') #extracts <a> tag from start _url
            link = x.xpath('.//@href').extract_first()  #extracts URL for the articles recursively
            yield response.follow(link, callback = self.parse_news)

        #For scraping the links on the next page of the website
        next_page = response.xpath('//link[@rel = "next"]/@href').extract_first()
        if next_page is not None:
           yield response.follow(next_page, callback = self.parse)

    #For scraping a particular article listed on the main page
    def parse_news(self,response):
        i = ZeeItem()
        i['headline'] = response.xpath('//h1[contains(@class, "article-heading margin")]/text()').extract_first() #scrapes headline
        i['datetime'] = response.xpath('//span[contains(@class, "date")]/text()').extract_first()[15:-4] #scrapes datetime
        i['image'] = response.xpath('//div[contains(@class, "field-item")]/img/@src').extract_first() #scrapes image url
        i['summary'] = response.xpath('//p[contains(@class, "margin")]/text()').extract_first() #scrapes summary of the news
        i['link'] = response.url
        yield i
