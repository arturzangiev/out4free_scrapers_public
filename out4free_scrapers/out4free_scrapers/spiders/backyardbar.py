# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class BackyardbarSpider(scrapy.Spider):
    name = "backyardbar"
    allowed_domains = ["backyardbar.co.uk"]
    start_urls = ['http://backyardbar.co.uk/events/upcoming/']

    def parse(self, response):
        urls = response.xpath('//h2[@class="tribe-events-list-event-title summary"]/a[@class="url"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h2[@class="tribe-events-single-event-title summary"]/text()').extract_first()
        description = response.xpath('//div[@class="tribe-events-single-event-description tribe-events-content entry-content description"]//text()').extract()
        description = " ".join(description)
        price = response.xpath('//span[@class="tribe-events-cost"]/text()').extract_first().strip()
        start_datetime = response.xpath('//span[@class="date-start dtstart"]/text()').extract_first()
        category_id = CatItem.django_model.objects.get(id=4)
        venue_id = VenueItem.django_model.objects.get(id=2)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="tribe-events-event-image"]//img/@src').extract_first()
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