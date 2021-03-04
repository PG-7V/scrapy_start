import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['parsemachine.com']
    start_urls = ['http://parsemachine.com/']
    page_count = 10


    def start_requests(self):
        for page in range(1, 1 + self.page_count):
            url = f'https://parsemachine.com/sandbox/catalog/?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.product-card .title::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response, **kwargs):
        item = {
            'url': response.request.url,
            'title': response.css('#product_name::text').extract_first('').strip(),
            'price': response.css('#product_amount::text').extract_first('').strip()
        }
        yield item
