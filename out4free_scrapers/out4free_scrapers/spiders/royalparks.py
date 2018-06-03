# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class RoyalparksSpider(scrapy.Spider):
    name = "royalparks"
    allowed_domains = ["royalparks.org.uk"]
    start_urls = ['https://www.royalparks.org.uk/parks/hyde-park/things-to-see-and-do/events-in-hyde-park/upcoming-events-in-hyde-park?query=&f.Park|B=Hyde+Park&f.Park|B=Kensington+Gardens&f.Park|B=Greenwich+Park&f.Park|B=St+James%27s+Park&f.Park|B=Bushy+Park&f.Park|B=Green+Park&f.Park|B=Brompton+Cemetery&f.Park|B=Richmond+Park&f.Park|B=The+Regent%27s+Park&f.Price|D=Free']

    def parse(self, response):
        urls = response.xpath('//h3[@class="latest-event-title"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="no-margin-top grey-text text-lighten-3 center"]/text()').extract_first()
        description = response.xpath('//div[@class="col s12"]/p/text()').extract()
        description = " ".join(description)
        price = 'free'
        start_datetime = response.xpath('//span[@itemprop="startDate"]/@content').extract_first()
        category_id = CatItem.django_model.objects.get(id=9)
        venue_name = response.xpath('//span[@itemprop="address"]/@content').extract_first()
        if "St James's Park" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=51)
        elif "Kensington Gardens" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=50)
        elif "Richmond Park" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=52)
        elif "Greenwich Park" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=53)
        elif "Hyde Park" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=54)
        elif "Bushy Park" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=55)
        elif "Green Park" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=56)
        elif "Brompton Cemetery" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=57)
        elif "The Regent's Park" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=58)
        else:
            venue_id = VenueItem.django_model.objects.get(id=41)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="col s12 m5"]/img/@src').extract_first()
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
