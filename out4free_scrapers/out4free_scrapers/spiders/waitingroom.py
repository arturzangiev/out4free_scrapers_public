# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class WaitingroomSpider(scrapy.Spider):
    name = "waitingroom"
    allowed_domains = ["lithiumpears.com"]
    start_urls = ['http://lithiumpears.com/lock/event-list/']

    def parse(self, response):
        urls = response.xpath('//h3[@class="event-title"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="gdlr-event-title"]/text()').extract_first()
        description = response.xpath('//div[@class="gdlr-event-content"]//text()').extract()
        description = " ".join(description)
        price = response.xpath('//div[@class="event-status-wrapper"]/span[@class="coming-soon"]/text()').extract_first()
        date = response.xpath('//div[@class="gdlr-info-date gdlr-info"]/text()').extract_first().strip()
        regex_date = re.sub(r"^(\d+) / (\w+) / (\d+)$", r"\1 \2 \3", date)
        time = response.xpath('//div[@class="gdlr-info-time gdlr-info"]/text()').extract_first().strip()
        regex_time = re.sub(r"^(\d+)(\w+)-(\d+\w+)$", r"\1 \2", time)
        start_datetime = regex_date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=12)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="gdlr-event-content"]//img/@src').extract_first()
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
