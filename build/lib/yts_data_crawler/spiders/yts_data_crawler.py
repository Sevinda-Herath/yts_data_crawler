from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class CrawlingSpider(CrawlSpider):
    name = 'yts'
    allowed_domains = ['yts.mx']
    start_urls = ['https://yts.mx/']

    rules = (
        Rule(LinkExtractor(allow='/movies/'), callback='parse', follow=True), 
    )

    def parse(self, response):
        runtime_text = ''.join(response.css('.row .tech-spec-element::text').getall()).replace(" ","").replace("\n","").replace("\xa0","")
        runtime = re.search(r'\d+hr\d+min', runtime_text).group(0) if re.search(r'\d+hr\d+min', runtime_text) else None

        yield {
            'URL': response.url,
            'MovieTitle': response.css('.hidden-xs h1::text').get(),
            'ReleasedYear': response.css('.hidden-xs h2::text').getall()[0],
            'MoviePoster': response.css('.row #movie-poster::text').getall()[0],
            'Genres': response.css('.hidden-xs h2::text').getall()[1],
            'MoviePosterSrc': response.css('.row #movie-poster img::attr(src)').get(),
            'YTSLikes': response.css('.rating-row #movie-likes::text').get(),
            'IMDbRating': response.css('.rating-row [itemprop="ratingValue"]::text').get(),
            'IMDbVotes': response.css('.rating-row [itemprop="ratingCount"]::text').get(),
            'MovieDirector': response.css('.list-cast-info [itemprop="director"] [itemprop="name"]::text').getall(),
            'Runtime': runtime,
            'Seeds': response.css('div.tech-spec-element.col-xs-20.col-sm-10.col-md-5 font::text').get(),
            'Uploader': response.css('#synopsis a::text').get(),
            'UploadedTime': response.css('#synopsis span em::text').get(),
        }
        
