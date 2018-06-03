# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class PrimobarSpider(scrapy.Spider):
    name = "primobar"
    allowed_domains = ["primobar.co.uk"]
    start_urls = ['http://primobar.co.uk/listen/']

    def parse(self, response):
        blocks = response.xpath('//article[@class="event-block blog wow fadeInUp"]')
        for block in blocks:
            url = block.xpath('.//a[@class="read-more pd-t-100 pd-b-50"]/@href').extract_first()
            date = block.xpath('./div[@class="eb__date wow slideInUp"]/h5/text()').extract_first()
            month = block.xpath('./div[@class="eb__date wow slideInUp"]/p/text()').extract_first()
            datetime = date + ' ' + month + ' 18:00:00'
            yield scrapy.Request(url, callback=self.individual_page, meta={'datetime': datetime})

    def individual_page(self, response):
        title = response.xpath('//h2[@class="txt-white"]/text()').extract_first()
        description = response.xpath('//div[@class="twothird pd-l-50"]//text()').extract()
        description = " ".join(description)
        price = response.xpath('//p[@class="pd-b-40"]/text()').extract()[-1]
        start_datetime = response.meta['datetime']
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=19)
        slug = slugify(title)
        image_urls = response.xpath('//section[@class="single-image__pullup"]/@content').extract_first()
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
