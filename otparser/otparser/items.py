# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_photo_links(photo_url):

    correct_url = photo_url.replace('w_40', 'w_2000').replace('h_40', 'h_2000').replace('d_photoiscoming', 'd_photoiscoming.png')
    return correct_url

class OtparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photo_links))
    _id = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    details = scrapy.Field(output_processor=TakeFirst())
