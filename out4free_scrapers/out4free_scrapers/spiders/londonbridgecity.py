# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class LondonbridgecitySpider(scrapy.Spider):
    name = "londonbridgecity"
    allowed_domains = ["londonbridgecity.co.uk"]
    start_urls = ['http://londonbridgecity.co.uk/events']

    def parse(self, response):
        urls = response.xpath('//div[@class="event-summary"]/h1/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//div[@class="col-10 content-block-text"]/h1/text()').extract_first()
        description = response.xpath('//div[@class="col-10 content-block-text"]/p/text()').extract()
        description = " ".join(description)
        price = 'free'
        date = response.xpath('//div[@class="col-10 content-block-text"]/span[@class="article-date"]/text()').extract_first()
        start_datetime = re.sub(r"^(\d+ \w+ \d+ \d+:\d+ \w{2}).*$", r"\1", date)
        category_id = CatItem.django_model.objects.get(id=5)
        venue_id = VenueItem.django_model.objects.get(id=31)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="col-10 content-block-text"]//img/@src').extract_first()
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
