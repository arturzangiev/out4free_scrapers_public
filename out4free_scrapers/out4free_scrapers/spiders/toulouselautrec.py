# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class ToulouselautrecSpider(scrapy.Spider):
    name = "toulouselautrec"
    allowed_domains = ["toulouselautrec.co.uk"]
    start_urls = ['https://www.toulouselautrec.co.uk/book-tickets']

    def parse(self, response):
        urls = response.xpath('//div[@class="event  event--1"]/a/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//div[@class="event-desc"]/h2/text()').extract_first().strip()
        description = response.xpath('//div[@class="event-desc"]/p//text()').extract()[13:]
        description = " ".join(description)
        price = response.xpath('//font[@size="4"]/font/text()').extract_first()
        date = response.url
        regex_date = re.sub(r"^.+?date=(\d+-\d+-\d+)$", r"\1", date)
        time = response.xpath('//font[@color="#00FA9A"]/font/text()').extract_first()
        regex_time = re.sub(r"^.+?(\d+\.*\d*)(am|pm)$", r"\1 \2", time).replace('.', ':')
        start_datetime = regex_date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=42)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="event-info"]/img/@src').extract_first()
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
