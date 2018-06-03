# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class RoundhouseSpider(scrapy.Spider):
    name = "roundhouse"
    allowed_domains = ["roundhouse.org.uk"]
    start_urls = ['http://www.roundhouse.org.uk/whats-on/list']

    def parse(self, response):
        urls = response.xpath('//a[@class="btn btn-more"]/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1/text()').extract_first()
        description = response.xpath('//article[@class="content-body"]/p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//p[@class="amount"]/span/text()').extract_first()
        start_datetime = response.xpath('//time[@itemprop="startDate"]/@datetime').extract_first()
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=96)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="main-image"]/img/@src').extract_first()
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
