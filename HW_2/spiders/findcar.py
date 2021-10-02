import scrapy
from ..items import CarItem


class FindcarSpider(scrapy.Spider):
    name = 'findcar'
    allowed_domains = ["autoria.com"]
    start_urls = ["https://auto.ria.com/uk/legkovie/tesla/"]
    page_count = 10

    def start_requests(self):
        for p in range(1, 1 + self.page_count):
            url = f"https://auto.ria.com/uk/legkovie/tesla/?page={p}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for car in response.css("div.content"):
            car_item = CarItem()
            link_car = car.css("a.address::attr(href)").get()
            vin = car.css('div.definition-data > div > span > span:nth-child(2)::text').get().replace('\u0445', '')
            car_item['model'] = car.css('span::text').get().strip(),
            car_item['year'] = car.css('a[class="address"]::text')[1].get().strip(),
            car_item['mileage'] = car.css('div.definition-data > ul > li.item-char.js-race::text').get().strip().\
                replace('\u0442\u0438\u0441. \u043a\u043c', '000'),
            car_item['priceUAH'] = car.css('div.price-ticket > span > span.i-block > span::text').get().strip(),
            car_item['priceUSD'] = car.css('div.price-ticket > span > span:nth-child(1)::text').get().strip(),
            car_item['vin'] = car.css('div.definition-data > div > span > span:nth-child(2)::text').get().strip() if vin else None,
            car_item['car_link'] = link_car
            yield car_item

        next_page = response.css("span.page-item > link::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
