# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class MagicgardenSpider(scrapy.Spider):
    name = "magicgarden"
    allowed_domains = ["magicgardenpub.com"]
    start_urls = ['http://www.magicgardenpub.com/events/']

    def parse(self, response):
        urls = response.xpath('//h2[@class="tribe-events-list-event-title entry-title summary"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h2[@class="tribe-events-single-event-title summary entry-title"]/text()').extract_first()
        description = response.xpath('//div[@class="tribe-events-single-event-description tribe-events-content entry-content description"]//p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//span[@class="tribe-events-cost"]/text()').extract_first()
        start_datetime = response.xpath('//span[@class="date-start dtstart"]/text()').extract_first()
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=8)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="tribe-events-event-image"]/img/@src').extract_first()
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
