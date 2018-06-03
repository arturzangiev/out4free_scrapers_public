# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class LondongovSpider(scrapy.Spider):
    name = "londongov"
    allowed_domains = ["london.gov.uk"]
    start_urls = ['https://www.london.gov.uk/events']

    def parse(self, response):
        urls = response.xpath('//div[@class="view-content"]/div/article/a/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="node--event--title title"]/text()').extract_first()
        description = response.xpath('//div[@class="field__items"]//text()').extract()
        description = " ".join(description)
        price = response.xpath('//span[@class="tickets"]/text()').extract_first()
        start_datetime = response.xpath('//div[@class="block__content"]/div/span[@class="time"]/time/@datetime').extract_first()
        category_id = CatItem.django_model.objects.get(id=5)
        venue_id = VenueItem.django_model.objects.get(id=18)
        slug = slugify(title)
        image_urls = response.xpath('//img[@class="gla-2-1-large"]/@src').extract_first()
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
