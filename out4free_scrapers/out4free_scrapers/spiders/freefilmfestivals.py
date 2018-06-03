# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify
import json


class FreefilmfestivalsSpider(scrapy.Spider):
    name = "freefilmfestivals"
    allowed_domains = ["freefilmfestivals.org"]
    start_urls = ['http://www.freefilmfestivals.org/whats-on/?view=list']

    def parse(self, response):
        urls = response.xpath('//div[@class="highlight-white"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="tribe-events-single-event-title"]/text()').extract_first()
        description = response.xpath('//div[@class="tribe-events-single-event-description tribe-events-content"]//text()').extract()
        description = " ".join(description)
        price = response.xpath('//span[@class="tribe-events-cost"]/text()').extract_first()
        date = response.xpath('//script[@type="application/ld+json"]/text()').extract_first()
        start_datetime = json.loads(date)[0].get('startDate')
        category_id = CatItem.django_model.objects.get(id=2)
        venue_id = VenueItem.django_model.objects.get(id=16)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="tribe-events-single-event-description tribe-events-content"]//img/@src').extract_first()
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
