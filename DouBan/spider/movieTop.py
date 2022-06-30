import scrapy
from DouBan.items import DoubanItem

class MovietopSpider(scrapy.Spider):
    name = 'movieTop'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response, **kwargs):
        movie_list = response.xpath('//*[@class="info"]')

        item = DoubanItem()
        for movie in movie_list:
            item['name'] = movie.xpath('./div[1]/a/span[1]/text()').extract_first()
            # item['person_info'] = movie.xpath('./*[@class="bd"]/p[1]/text()[1]').extract_first()
            # item['score'] = movie.xpath('./*[@class="rating_num"]/text()').extract_first()
            # item['desc'] = movie.xpath('./*[@class="inq"]/text()').extract_first()
            yield item

        # 翻页
        url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        if url is not None:
            url = response.urljoin(url)
            yield scrapy.Request(
                url=url
            )


