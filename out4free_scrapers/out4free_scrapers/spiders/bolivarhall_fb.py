# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify
import json
from urllib.parse import urlencode
from .. import api_keys


class BolivarHallFB(scrapy.Spider):
    name = "bolivarhall_fb"
    allowed_domains = ["graph.facebook.com"]

    def start_requests(self):
        api_domain = 'https://graph.facebook.com/'
        page_id = '102408299831992'
        endpoint = '/events?'
        params = {
                    "fields": ["cover", "id", "category", "description", "name", "place", "start_time"],
                    "access_token": api_keys.access_token
                 }

        full_request = api_domain + page_id + endpoint + urlencode(params)
        yield scrapy.Request(full_request, callback=self.parse)

    def parse(self, response):
        json_data = json.loads(response.body_as_unicode())
        events = json_data['data']
        for event in events:
            title = event.get('name')
            description = event.get('description')
            price = description
            start_datetime = event.get('start_time')
            event_url = 'https://www.facebook.com/events/' + event.get('id')
            category_id = CatItem.django_model.objects.get(id=6)
            venue_id = VenueItem.django_model.objects.get(id=61)
            slug = slugify(title)
            image_urls = event['cover']['source']

            fields = EventItem(title=title,
                               description=description,
                               price=price,
                               published=1,
                               start_date=start_datetime,
                               event_url=event_url,
                               category=category_id,
                               venue=venue_id,
                               slug=slug,
                               seo_title=title,
                               seo_description=description,
                               image_urls=[image_urls]
                               )

            yield fields
