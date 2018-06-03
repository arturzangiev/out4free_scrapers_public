# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import django
django.setup()
from scrapy_djangoitem import DjangoItem
from london.models import Event, Cat, Venue


class EventItem(DjangoItem, scrapy.Item):
    django_model = Event
    image_urls = scrapy.Field()
    images = scrapy.Field()
    # image_paths = scrapy.Field()


class CatItem(DjangoItem):
    django_model = Cat


class VenueItem(DjangoItem):
    django_model = Venue


# class MyItem(scrapy.Item):
#     image_urls = scrapy.Field()
#     images = scrapy.Field()