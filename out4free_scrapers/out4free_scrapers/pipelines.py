# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from .items import EventItem
from django.utils import timezone
import dateparser, datetime


class PricePipeline(object):
    def process_item(self, item, spider):
        if item['price'] is not None and re.search('free|pay what you want|pwyw|No tickets required|^0\.00$', item['price'], re.IGNORECASE):
            return item
        else:
            raise DropItem("Not Free event %s" % item)


class TextFixPipeline(object):
    def process_item(self, item, spider):
        item['title'] = item['title'].strip()[:200]
        item['description'] = item['description'].strip()[:1000]
        item['seo_title'] = item['seo_title'].strip()[:50]
        item['seo_description'] = item['seo_description'].strip()[:160]
        item['slug'] = item['slug'].strip()[:50]
        item['price'] = item['price'].strip()[:20]
        item['start_date'] = dateparser.parse(item['start_date'])
        item['end_date'] = item['start_date'] + datetime.timedelta(hours=2) if item['start_date'] is not None else None
        return item


class DuplicatePipeline(object):
    def process_item(self, item, spider):
        all_events = EventItem.django_model.objects
        if all_events.filter(slug=item['slug']).exists():
            duplicate_event = all_events.get(slug=item['slug'])
            if duplicate_event.start_date is not None and duplicate_event.start_date < timezone.now():
                # if the date of event in DB is less then now delete from DB and return new item
                duplicate_event.delete()
                return item
            else:
                # if date of event in DB not less then now consider duplicate
                raise DropItem("Duplicate event")
        else:
            return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            if image_url is not None:
                yield scrapy.Request(image_url)
            else:
                raise DropItem("There is no image link")

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image'] = 'london/' + image_paths[0]
        item.save()
        return item