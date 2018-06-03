# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class OldbluelastSpider(scrapy.Spider):
    name = "oldbluelast"
    allowed_domains = ["theoldbluelast.com"]
    start_urls = ['http://www.theoldbluelast.com/listings/']

    def parse(self, response):
        blocks = response.xpath('//ol[@class="listings"]/li[div[@class="listings_night_info"]]')
        for block in blocks:
            title = block.xpath('./div[@class="listings_night_info"]/b/text()').extract_first()
            description = block.xpath('./div[@class="listings_night_info"]/p/text()').extract()
            description = " ".join(description)
            price = block.xpath('./ul[@class="listings_details"]/li[2]/text()').extract_first()
            date = block.xpath('./ul[@class="listings_details"]/li[@class="listings_date"]/text()').extract()
            date = " ".join(date)
            time = block.xpath('./ul[@class="listings_details"]/li[3]/em/text()').extract_first()
            regex_time = re.sub(r"^(.+?)\s*-\s*.+?$", r"\1", time).replace('.', ':')
            start_datetime = date + ' ' + regex_time
            category_id = CatItem.django_model.objects.get(id=1)
            venue_id = VenueItem.django_model.objects.get(id=45)
            slug = slugify(title)
            image_urls = block.xpath('./div[@class="listings_image"]/img/@src').extract_first()

            fields = EventItem(title=title,
                               description=description,
                               price=price,
                               published=1,
                               start_date=start_datetime,
                               event_url=response.url,
                               category=category_id,
                               venue=venue_id,
                               slug=slug,
                               seo_title=title,
                               seo_description=description,
                               image_urls=[image_urls]
                               )

            yield fields