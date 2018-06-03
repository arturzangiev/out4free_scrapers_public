# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class OvalhouseSpider(scrapy.Spider):
    name = "ovalhouse"
    allowed_domains = ["ovalhouse.com"]
    start_urls = ['http://www.ovalhouse.com/whatson']

    def parse(self, response):
        urls = response.xpath('//ul[@class="links"]/li[contains(., "Info")]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//div[@id="info"]/header/h1/text()').extract_first()
        description = response.xpath('//section[@id="infotabs-1"]/p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//div[@id="ticketInfo"]/ul/li/text()').extract()
        price = " ".join(price)
        start_datetime = response.xpath('//section[@id="infotabs-4"]/ul/li/text()').extract_first()
        category_id = CatItem.django_model.objects.get(id=6)
        venue_id = VenueItem.django_model.objects.get(id=91)
        slug = slugify(title)
        image_urls = response.xpath('//figure[@id="mainImage"]/img/@src').extract_first()
        image_urls = response.urljoin(image_urls)
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
