# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class HelleniccentreSpider(scrapy.Spider):
    name = "helleniccentre"
    allowed_domains = ["helleniccentre.org"]
    start_urls = ['http://helleniccentre.org/events-culture/']

    def parse(self, response):
        urls = response.xpath('//h2[@class="subTitle"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="pageTitle"]/text()').extract_first()
        description = response.xpath('//div[@class="section__main"]//text()').extract()
        description = " ".join(description)
        description = description.strip()
        price = response.xpath('//div[@class="banner__item"]/p/text()').extract()
        price = " ".join(price)
        date = response.xpath('//div[@class="dateStack"]/span/text()').extract()
        date = " ".join(date)
        regex_date = re.sub(r"^.*?(\d{2}\s\w{3}\s\d{4}).*?$", r"\1", date)
        time = response.xpath('//div[@class="banner__item" and contains(h3, "Times")]/p/text()').extract_first()
        regex_time = re.sub(r"^.*?(\d{1,2}[\., ]*\d{1,2})\s*(am|pm).*$", r"\1 \2", time).replace('.', ':')
        start_datetime = regex_date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=6)
        venue_id = VenueItem.django_model.objects.get(id=127)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="section__lateral"]//img/@src').extract_first()
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
