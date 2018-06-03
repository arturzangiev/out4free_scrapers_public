# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class RochesterkinoSpider(scrapy.Spider):
    name = "rochesterkino"
    allowed_domains = ["rochesterkino.co.uk"]
    start_urls = ['http://www.rochesterkino.co.uk/screenings/category/london']

    def parse(self, response):
        urls = response.xpath('//a[@class="blog-title-link blog-link"]/@href').extract()
        for url in urls:
            url = re.sub(r"^\/\/(.+)$", r"http://\1", url)
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h2[@class="blog-title"]/a/text()').extract_first()
        description = response.xpath('//div[@class="paragraph"]//text()').extract()
        description = " ".join(description)
        price = description
        date = response.xpath('//span[@class="date-text"]/text()').extract_first().strip()
        regex_time = re.sub(r"^.*?(\d{1,2}).(\d{1,2})\s*(am|pm).*$", r"\1:\2 \3", description)
        start_datetime = date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=2)
        venue_id = VenueItem.django_model.objects.get(id=44)
        slug = slugify(title)
        image_urls = response.urljoin(response.xpath('//div[@class="wsite-image wsite-image-border-none "]/a/img/@src').extract_first())
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
