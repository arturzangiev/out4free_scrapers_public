# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class RoyalalberthallSpider(scrapy.Spider):
    name = "royalalberthall"
    allowed_domains = ["royalalberthall.com"]
    start_urls = ['https://www.royalalberthall.com/tickets/']

    def parse(self, response):
        urls = response.xpath('//h3[@class="title"]/a/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="title"]/text()').extract_first()
        description = response.xpath('//section[@class="unit unit-page-content details"]//text()').extract()
        description = " ".join(description)
        price = response.xpath('//span[@class="book-status"]/text()').extract_first()
        date = response.xpath('//div[@itemprop="startDate"]/text()').extract_first()
        time = response.xpath('//div[@class="date-description__start"]/text()').extract_first().strip()
        regex_time = re.sub(r"^Starts: (\d+:\d+)(am|pm)$", r"\1 \2", time)
        start_datetime = date + " " + regex_time
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=130)
        slug = slugify(title)
        image_urls = response.xpath('//meta[@property="og:image"]/@content').extract_first()
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
