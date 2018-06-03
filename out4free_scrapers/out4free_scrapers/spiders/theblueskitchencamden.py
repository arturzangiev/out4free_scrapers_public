# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class BlueskitchencamdenSpider(scrapy.Spider):
    name = "blueskitchencamden"
    allowed_domains = ["theblueskitchen.com"]
    start_urls = ['http://theblueskitchen.com/camden/listings/']

    def parse(self, response):
        urls = response.xpath('//a[@class="event-loader"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="whats-on-title"]/text()').extract_first()
        description = response.xpath('//div[@class="description grid_17"]/p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//h3[@class="start-time"]/text()').extract_first()
        date = response.xpath('//div[@class="event-date camden"]/small/text()').extract()
        date = " ".join(date)
        time = response.xpath('//h3[@class="start-time"]/text()').extract_first()
        regex_time = re.sub(r"^.*?(\d+:*\d*)\s*(AM|PM).*$", r"\1 \2", time)
        start_datetime = date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=47)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="slider bookings-slider-wrap grid_24"]//img/@src').extract_first()
        youtube = response.xpath('//body').re_first('youtube.com/(?:embed//*|watch\?v=)([A-Za-z0-9_-]+)')

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
