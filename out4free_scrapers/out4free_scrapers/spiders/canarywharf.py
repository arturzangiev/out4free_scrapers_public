# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class CanarywharfSpider(scrapy.Spider):
    name = "canarywharf"
    allowed_domains = ["canarywharf.com"]
    start_urls = ['http://canarywharf.com/arts-events/events/']

    def parse(self, response):
        urls = response.xpath('//a[@class="read-more"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="entry-title large"]/text()').extract_first()
        description = response.xpath('//div[@class="entry-content"]/p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//div[@id="secondary"]/p/text()').extract()[-1].strip()
        date = response.xpath('//div[@class="event-time"]/p/text()').extract_first()
        regex_date = re.sub(r"^(\w+ \d+ \w+)( - \w+ \d+ \w+)?$", r"\1", date)
        time = response.xpath('//div[@id="secondary"]/p/text()').extract()[0].strip()
        regex_time = re.sub(r"^(\d+\.*\d*)(-\d+\.*\d*)?(am|pm)$", r"\1 \3", time).replace('.', ':').replace('Daily', '12:00:00')
        start_datetime = regex_date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=5)
        venue_id = VenueItem.django_model.objects.get(id=43)
        slug = slugify(title)
        image_urls = response.xpath('//img[@class="attachment-slider-image"]/@src').extract_first()
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
