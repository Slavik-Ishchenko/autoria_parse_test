# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from items import CarItem


class Hw2Pipeline:
    def process_item(self, item, spider):
        adapter = CarItem(item)
        if adapter.get('priceUAH'):
            adapter['priceUAH'] = adapter['priceUAH'] * self.vat_factor
            return item
        else:
            raise DropItem(f"Missing priceUAH in {item}")

