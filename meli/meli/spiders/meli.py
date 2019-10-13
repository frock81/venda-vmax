import scrapy

class MeliSpider(scrapy.Spider):
    name = 'meli'
    start_urls = [
        'https://lista.mercadolivre.com.br/yamaha-vmax-1200-1995#D[A:yamaha%\
        20vmax%201200%201995]'
    ]

    def parse(self, response):
        for result in response.css('.item__info-link'):
            year, mileage = (x.strip() for x in result.css('.item__attrs::text')
                .get().split('|'))
            yield {
                'title': result.css('.main-title::text').get().strip(),
                'value': result.css('.price__fraction::text').get(),
                'year': year,
                'mileage': mileage,
                'location': result.css('.item__location::text').get()
            }
            next_page = result.css('a::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseLink)

    def parseLink(self, response):
        yield {
            'description': response.css('#description-includes p::text').get()
        }


