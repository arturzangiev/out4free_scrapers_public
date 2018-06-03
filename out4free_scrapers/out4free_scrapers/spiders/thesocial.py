# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class SocialSpider(scrapy.Spider):
    name = "social"
    allowed_domains = ["thesocial.com"]
    start_urls = ['http://www.thesocial.com/events/']

    def parse(self, response):
        urls = response.xpath('//tbody/tr/td/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="title"]/text()').extract_first()
        description = response.xpath('//div[@class="entry"]/p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//p[strong="Price"]//text()').extract()
        price = " ".join(price)
        date_time = response.xpath('//p[strong="Date/Time"]//text()').extract()
        date_time = " ".join(date_time).strip()
        start_datetime = re.sub(r"^.*?(\d{1,2}\s\w{3}\s\d{4}).+?(\d{1,2}:\d{2} \w{2}).*?$", r"\1 \2", " ".join(date_time.split()))
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=15)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="entry"]//img/@src').extract_first()
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
