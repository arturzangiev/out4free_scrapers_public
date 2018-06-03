# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify
from scrapy.selector import Selector
from selenium import webdriver
import time
import json


class AngelcomedySpider(scrapy.Spider):
    name = "angelcomedy"
    allowed_domains = ["angelcomedy.co.uk"]
    start_urls = ['http://www.angelcomedy.co.uk/camden-head/']

    def __init__(self):
        self.driver = webdriver.PhantomJS('/home/ubuntu/out4free_scrapers/phantomjs')

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(15)
        page_html = Selector(text=self.driver.page_source)
        urls = page_html.xpath('//a[contains(@class, "event")]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)
        self.driver.close()

    def individual_page(self, response):
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        json_str = response.xpath('//script[@type="application/ld+json"]/text()').extract_first()
        json_data = json.loads(json_str)
        description = json_data.get('description')
        price = json_data['offers'][0]['price']
        start_datetime = json_data.get('startDate')
        category_id = CatItem.django_model.objects.get(id=4)
        venue_name = json_data['location']['name']
        if "The Bill Murray" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=60)
        elif "The Camden Head" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=59)
        slug = slugify(title)
        image_urls = response.xpath('//img[@class="attachment-full-page size-full-page wp-post-image"]/@src').extract_first()
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
