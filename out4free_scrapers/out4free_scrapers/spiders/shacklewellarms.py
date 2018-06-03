# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class ShacklewellarmsSpider(scrapy.Spider):
    name = "shacklewellarms"
    allowed_domains = ["shacklewellarms.com"]
    start_urls = ['http://www.shacklewellarms.com/listings/']

    def parse(self, response):
        urls = response.xpath('//a[@class="GridBlock"]/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="EventDetailTitle-title"]/text()').extract_first()
        description = response.xpath('//div[@class="EventDetailDescription"]//text()').extract()
        description = " ".join(description)
        price = response.xpath('//span[@class="EventDetailPrice-price"]/text()').extract_first().strip()
        start_datetime = response.xpath('//time[@class="EventDetailTimeAndVenue-doorsOpen"]/@datetime').extract_first()
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=9)
        slug = slugify(title)
        image_urls = response.xpath('//script[@type="application/ld+json"]/text()').extract_first()
        image_urls = re.sub(r"^.+?image&quot;:&quot;(.+?)&quot;.+$", r"\1", image_urls)
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
