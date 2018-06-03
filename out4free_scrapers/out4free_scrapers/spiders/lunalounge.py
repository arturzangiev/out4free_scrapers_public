# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class LunaloungeSpider(scrapy.Spider):
    name = "lunalounge"
    allowed_domains = ["lunalounge.info"]
    start_urls = ['http://www.lunalounge.info/']

    def parse(self, response):
        urls = response.xpath('//a[@class="progression-button view-event-btn-pro"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//div[@class="events-container-single"]/h2/text()').extract_first()
        description = response.xpath('//div[@class="entry-content description"]//text()').extract()
        description = " ".join(description)
        price = response.xpath('//span[@class="ticket-name"]/text()').extract_first()
        start_datetime = response.xpath('//abbr[@class="dtstart"]/@title').extract_first()
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=32)
        slug = slugify(title)
        image_urls = response.xpath('//img[@class="attachment-progression-events wp-post-image"]/@src').extract_first()
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
