# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class HouseofvansSpider(scrapy.Spider):
    name = "houseofvans"
    allowed_domains = ["houseofvanslondon.com"]
    start_urls = ['http://houseofvanslondon.com/events/calendar/embed-list/film',
                  'http://houseofvanslondon.com/events/calendar/embed-list/film?after=1']

    def parse(self, response):
        urls = response.xpath('//ul/li/a/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="event-name"]/text()').extract_first()
        description = response.xpath('//div[@class="event-description"]//text()').extract()
        description = " ".join(description)
        price = description
        start_datetime = response.xpath('//div[@id="event-countdown"]/@data-starts').extract_first()
        category_id = CatItem.django_model.objects.get(id=2)
        venue_id = VenueItem.django_model.objects.get(id=6)
        slug = slugify(title)
        image_urls = response.xpath('substring-before(substring-after(//div[contains(@class, "events-gallery")]/@style, "("), ")")').extract_first()
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
