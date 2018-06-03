# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class StrawberrytoursSpider(scrapy.Spider):
    name = "strawberrytours"
    allowed_domains = ["strawberrytours.com"]
    start_urls = ['https://strawberrytours.com/london/tours']

    def parse(self, response):
        urls = response.xpath('//div[@class="image_box_item_inner2"]/a/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//div[@class="TourTitle"]/text()').extract()
        title = " ".join(title).strip()
        description = response.xpath('//div[@class="article-body"]/p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//div[@class="TourTitleMid"]/ul/li[contains(strong, "Price")]/text()').extract_first().strip()
        start_datetime = response.xpath('//body').re_first('"startDate": "(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})"')
        category_id = CatItem.django_model.objects.get(id=9)
        venue_id = VenueItem.django_model.objects.get(id=49)
        slug = slugify(title)
        image_urls = response.xpath('//img[@class="GalleryImage"]/@src').extract_first()
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
