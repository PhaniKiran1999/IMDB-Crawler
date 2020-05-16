import scrapy
from scrapy.crawler import CrawlerProcess
import urllib.request 
# from scrapy.selector import Selector 

class IMDB_Spider(scrapy.Spider):
	name = 'imdb_spider'
	count = 0
	def start_requests(self):
		url = "https://www.imdb.com/name/nm0301959/mediaindex?ref_=nm_ql_3"#lenord
		# urls = ["https://www.imdb.com/name/nm0301959/mediaindex?ref_=nm_ql_3"#lenord,
		# "https://www.imdb.com/name/nm0192505/mediaindex?ref_=nm_ql_3"#penny,
		# "https://www.imdb.com/name/nm0374865/mediaindex?ref_=nm_ql_3"#howard,
		# "https://www.imdb.com/name/nm2471798/mediaindex?ref_=nm_ql_3"#raj]
		# for url in urls:
		# 	yield  scrapy.Request(url = url, callback = self.parse_front)
		yield  scrapy.Request(url = url, callback = self.parse_front)

	def parse_front(self, response):
		urls = response.xpath('//span[@class = "page_list"]//a/@href').extract()
		for url in urls:
			url = "https://www.imdb.com"+url
			yield response.follow(url = url, callback = self.parse_pages)

	def parse_pages(self, response):
		image_links = response.xpath('//div[@class = "media_index_thumb_list"]//a/img/@src').extract()

		img_urls = []
		for url in image_links:
			temp = url.split("@")
			temp = temp[0]+"@._V1_QL50_.jpg"
			img_urls.append(temp)

		for img_url in img_urls:
			file_path = "C:\\Users\\phani\\OneDrive\\Desktop\\project-ideas\\Images\\lenord\\"
			downloaded_image = open(file_path+str(self.count)+".jpg", "wb")
			image_on_web = urllib.request.urlopen(img_url)
			while True:
				buf = image_on_web.read(65536)
				if len(buf) == 0:
					break
				downloaded_image.write(buf)
			downloaded_image.close()
			image_on_web.close()
			self.count += 1   


process = CrawlerProcess()
process.crawl(IMDB_Spider)
process.start()