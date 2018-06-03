# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class BritishmuseumSpider(scrapy.Spider):
    name = "britishmuseum"
    allowed_domains = ["britishmuseum.org"]
    start_urls = ['http://www.britishmuseum.org/whats_on/events_calendar.aspx']

    def parse(self, response):
        urls = response.xpath('//p[@class="pullOut title"]/a/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//div[@class="grid_4 alpha"]/h1/text()').extract()
        title = " ".join(title)
        description = response.xpath('//div[@class="grid_4"]/p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//p[@class="pullOut"]/span[@class="highlight"]/text()').extract_first()
        date = response.xpath('//p[@class="pullOut"]/text()').extract_first()
        time = response.xpath('//p[@class="pullOut"]/text()').extract()[1].strip()
        regex_time = re.sub(r"^(\d+)\.(\d+)–\d+\.\d+$", r"\1:\2", time)
        start_datetime = date + ' ' + regex_time
        category_id = CatItem.django_model.objects.get(id=6)
        venue_id = VenueItem.django_model.objects.get(id=17)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="grid_4 omega"]/img/@src').extract_first()
        image_urls = response.urljoin(image_urls)

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
                           image_urls=[image_urls]
                           )

        yield fields
