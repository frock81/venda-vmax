import scrapy
import os

class MeliSpider(scrapy.Spider):
    name = 'meli'
    start_urls = [
        'https://lista.mercadolivre.com.br/yamaha-vmax-1200-1995#D[A:yamaha%\
        20vmax%201200%201995]'
    ]
    csv_filename = 'meli.csv'

    def parse(self, response):
        os.remove(self.csv_filename)
        with open(self.csv_filename, 'w') as csv_file:
            csv_file.write("mileage;description;title;price;location;year\n".encode('utf-8'))
        for result in response.css('.item__info-link'):
            year, mileage = (x.strip() for x in result.css('.item__attrs::text')
                .get().split('|'))
            obj = {
                'title': result.css('.main-title::text').get().strip(),
                'price': result.css('.price__fraction::text').get(),
                'year': year,
                'mileage': mileage,
                'location': result.css('.item__location::text').get()
            }
            next_page = result.css('a::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseLink,
                    cb_kwargs=dict(obj=obj))

    def parseLink(self, response, obj):
        obj['description'] = response.css('#description-includes p::text').get()
        str = ''
        objLen = len(obj)
        i = 1
        for field in obj:
            # yield {'field': field, 'i': i, 'value': obj[field]}
            if obj[field] != None:
                if i == objLen:
                    str += "'" + obj[field] + "'\n"
                else:
                    str += "'" + obj[field] + "';"
            else:
                if i == objLen:
                    str += "''\n"
                else:
                    str += "'';"
            i += 1
        with open('meli.csv', 'a') as csv_file:
            csv_file.write(str.encode('utf-8'))
        yield obj


