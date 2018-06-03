# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify
from scrapy.selector import Selector
from selenium import webdriver
import time


class SkygardenSpider(scrapy.Spider):
    name = "skygarden"
    allowed_domains = ["bookingbug.com"]
    start_urls = ['https://bespoke.bookingbug.com/skygarden/new_booking.html#/events']

    def __init__(self):
        self.driver = webdriver.PhantomJS('/home/ubuntu/out4free_scrapers/phantomjs')

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(15)
        page_html = Selector(text=self.driver.page_source)
        title = 'Free visit to SkyGarden'
        description = 'Known as the walkie talkie due to its unique shape, this skyscraper features a top-floor restaurant and bar. Press on more information about the event and book your free visit.'
        price = 'free'
        date = page_html.xpath('//h2/text()').extract_first()
        start_datetime = re.sub(r"^.+? (\d+\w{2} \w+ \d+)$", r"\1 23:00:00", date)
        category_id = CatItem.django_model.objects.get(id=3)
        venue_id = VenueItem.django_model.objects.get(id=1)
        slug = slugify(title)
        image_urls = 'https://out4free-static-files.s3.amazonaws.com/media/london/full/skygarden.jpg'
        youtube = 'Rd-V2D07XOM'

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
