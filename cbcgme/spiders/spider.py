import scrapy

from scrapy.loader import ItemLoader
from ..items import CbcgmeItem
from itemloaders.processors import TakeFirst


class CbcgmeSpider(scrapy.Spider):
	name = 'cbcgme'
	start_urls = ['https://www.cbcg.me/me/javnost-rada/aktuelno/saopstenja',
	              'https://www.cbcg.me/me/javnost-rada/aktuelno/dogadjaji']

	def parse(self, response):
		post_links = response.xpath('//div[@class="news-listing-item"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[text()="»"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="page-text"]//text()[normalize-space() and not(ancestor::dvi[@class="d-flex"] | ancestor::p[@class="mb-3 t-blue"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="mb-3 t-blue"]/text()').get()

		item = ItemLoader(item=CbcgmeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
