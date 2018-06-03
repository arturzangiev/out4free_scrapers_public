# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class TopsecretcomedyclubSpider(scrapy.Spider):
    name = "topsecretcomedyclub"
    allowed_domains = ["thetopsecretcomedyclub.co.uk"]
    start_urls = ['http://thetopsecretcomedyclub.co.uk/events-listings/']

    def parse(self, response):
        urls = response.xpath('//a[@class="info-button"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="main-title"]/text()').extract_first()
        description = response.xpath('//div[@class="event-featured-comedians"]/a/text()').extract_first()
        price = response.xpath('//span[@class="event-prices"]/text()').extract_first()
        date = response.xpath('//h2[@class="main-subtitle"]/text()').extract_first()
        time = response.xpath('//span[@class="event-time"]/text()').extract_first().replace('.', ':')
        start_datetime = date + ' ' + time
        category_id = CatItem.django_model.objects.get(id=4)
        venue_id = VenueItem.django_model.objects.get(id=4)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="event-featured-comedians"]/a/img/@src').extract_first()
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
