# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class RichmixSpider(scrapy.Spider):
    name = "richmix"
    allowed_domains = ["richmix.org.uk"]
    start_urls = ['https://www.richmix.org.uk/events']

    def parse(self, response):
        urls = response.xpath('//a[@class="more-info"]/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="page__title title"]/text()').extract_first().strip()
        description = response.xpath('//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]/div[@class="field-items"]/div[@class="field-item even"]/p/text()').extract()[6:-1]
        description = " ".join(description)
        price = response.xpath('//div[@class="field field-name-field-maximum-price field-type-number-decimal field-label-hidden"]/div[@class="field-items"]/div[@class="field-item even"]/text()').extract_first()
        start_datetime = response.xpath('//div[@class="field field-name-field-date field-type-datetime field-label-hidden"]/div[@class="field-items"]/div[@class="field-item even"]/span[@class="date-display-single"]/@content').extract_first()
        category_id = CatItem.django_model.objects.get(id=6)
        venue_id = VenueItem.django_model.objects.get(id=23)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="field field-name-field-banner-image field-type-image field-label-hidden"]/div[@class="field-items"]/div[@class="field-item even"]/img/@src').extract_first()
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
