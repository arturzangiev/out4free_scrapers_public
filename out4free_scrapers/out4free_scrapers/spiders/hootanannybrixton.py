# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class HootanannybrixtonSpider(scrapy.Spider):
    name = "hootanannybrixton"
    allowed_domains = ["hootanannybrixton.co.uk"]
    start_urls = ['http://www.hootanannybrixton.co.uk/#whatson']

    def parse(self, response):
        urls = response.xpath('//div[@class="band"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h2[@class="page-title entry-title"]/text()').extract_first()
        description = response.xpath('//div[@class="band1txtwide"]/p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//div[@class="band1txtwide"]/h5/text()').extract_first()
        date = response.xpath('//h3/text()').extract_first()
        time = response.xpath('//div[@class="band1txtwide"]/h5/text()').extract()[2].strip()
        regex_time = re.sub(r"^Time: (\d+)(am|pm).*$", r"\1 \2", time)
        start_datetime = date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=33)
        slug = slugify(title)
        image_urls = response.xpath('//img[@class="attachment-medium size-medium"]/@src').extract_first()
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
