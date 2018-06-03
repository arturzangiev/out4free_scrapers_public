# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class LocksidecamdenSpider(scrapy.Spider):
    name = "locksidecamden"
    allowed_domains = ["locksidecamden.com"]
    start_urls = ['http://www.locksidecamden.com/whats-on/']

    def parse(self, response):
        urls = response.xpath('//a[@class="thumb js-coll-port-lightbox"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="title-text"]/text()').extract_first()
        description = response.xpath('//div[@class="title-wrapper"]/p/text()').extract()
        description = " ".join(description)
        price = description
        date = response.xpath('//h3[@class="subtitle-text"]/text()').extract_first()
        time = response.xpath('//div[@class="title-wrapper"]/p/text()').extract_first()
        regex_time = re.sub(r"^(\d+\.\d+).*$", r"\1", time).replace('.', ':')
        start_datetime = date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=48)
        slug = slugify(title)
        image_urls = response.xpath('//div[@id="poster-container"]/img/@src').extract_first()
        youtube = response.xpath('//body').re_first('youtube.com/(?:embed/|watch\?v=)([A-Za-z0-9_-]+)')

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
                           youtube=youtube,
                           image_urls=[image_urls]
                           )

        yield fields
