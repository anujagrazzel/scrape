import scrapy
from cnn.items import CnnItem

class cnnspider(scrapy.Spider):
     name='cnn'
     allowed_domain = ['http://money.cnn.com']
     start_urls = ['http://money.cnn.com']
     #clones the repo
     #def parse(self , response):
         #filename = response.url.split("/")[-2] + '.html'
         #with open(filename, 'wb') as f:
             #f.write(response.body)


def __init__(self, pages=2, *args, **kwargs):
        super(cnn, self).__init__(*args, **kwargs)
        for count in range(1 , int(pages)+1):
        	self.start_urls.append('http://money.cnn.com/technology/?iid=Tech_Nav'+ str(count))
def start_requests(self):
	 for url in self.start_urls:
         	yield scrapy.Request(url, callback = self.parse)

def parse(self, response):
         blocks = response.xpath('//div/div[contains(@class,"_1uNWB")]')
	 for block in blocks:
         	link = block.xpath('./div[1]/div[2]/a/@href')
                yield response.follow(link, callback = self.parse_content)


         def parse_content(self, response):
             i = CnnItem()
             i["headlines"] = response.xpath("//h1/text()").extract_first()
             yield i
