# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class HattrickproductionsSpider(scrapy.Spider):
    name = "hattrickproductions"
    allowed_domains = ["tickettext.co.uk"]
    start_urls = ['https://hat-trick-productions.tickettext.co.uk/hat-trick-productions/']

    def parse(self, response):
        urls = response.xpath('//div[@class="event-button"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h1[@class="event-name"]/text()').extract_first()
        description = response.xpath('//h1[@class="event-name"]/text()').extract_first()
        price = response.xpath('//span[@class="tier-free"]/strong/text()').extract_first()
        date = response.xpath('//h3[@class="event-date"]/text()').extract_first()
        time = response.xpath('//div[@class="meta"]/dl[@class="event"]/dd/text()').extract_first()
        regex_time = re.sub(r"^(\d+:\d+) – \d+:\d+$", r"\1", time)
        start_datetime = date + regex_time
        category_id = CatItem.django_model.objects.get(id=8) #8
        venue_name = response.xpath('//h3[@class="event-location"]/a/text()').extract_first()

        if "Princess Studio" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=126)
        elif "York Hall" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=125)
        elif "Wimbledon Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=124)
        elif "White Rabbit Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=123)
        elif "Waterloo East Theatre" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=122)
        elif "Wapping Hydraulic Power Station" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=121)
        elif "Viacom Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=120)
        elif "Under the Bridge" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=119)
        elif "Truman Brewery" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=118)
        elif "Trafalgar Square" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=117)
        elif "Town Hall Hotel" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=116)
        elif "Tobacco Dock" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=115)
        elif "Ticket Exchange Point" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=114)
        elif "Theatre Royal Stratford" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=113)
        elif "Theatre Royal Drury Lane" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=112)
        elif "The Troxy" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=111)
        elif "The Tabernacle Theatre" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=110)
        elif "The Phoenix" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=109)
        elif "The SSE Arena" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=108)
        elif "The LookOut" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=107)
        elif "The London Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=106)
        elif "The London Palladium" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=105)
        elif "The Invisible Dot" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=104)
        elif "The Hospital Club Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=103)
        elif "The Hackney Empire" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=102)
        elif "The Dominion Theatre" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=101)
        elif "Stephen Street Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=100)
        elif "Sky Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=99)
        elif "Silver Road Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=98)
        elif "Royal Airforce Memorial" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=97)
        elif "Roundhouse" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=96)
        elif "Riverside Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=95)
        elif "Ram Brewery" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=94)
        elif "RADA Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=93)
        elif "Queen Elizabeth Foyer" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=92)
        elif "Ovalhouse" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=91)
        elif "One Mayfair" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=90)
        elif "Olympia Two" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=89)
        elif "O2 Arena" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=88)
        elif "Morrison's Car Park" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=87)
        elif "Merchant Taylors' Hall" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=86)
        elif "London Coliseum" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=85)
        elif "London Aquatics Centre" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=84)
        elif "Linden House" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=83)
        elif "LH2 Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=82)
        elif "Leather Bottle" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=81)
        elif "KoKo Nightclub" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=80)
        elif "Kings Place" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=79)
        elif "Hammersmith Club" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=78)
        elif "Hammersmith Apollo" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=77)
        elif "Greenwood Theatre" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=76)
        elif "Gfinity Arena" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=75)
        elif "ExCeL London" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=74)
        elif "Earls Court" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=73)
        elif "Earl's Court Two" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=72)
        elif "Ealing studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=71)
        elif "Central Hall Westminster" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=70)
        elif "Cadogan Hall" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=69)
        elif "Cactus TV Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=68)
        elif "Butler's Wharf Pier" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=67)
        elif "3 Mills Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=66)
        elif "Build Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=65)
        elif "Auriol Kensington Rowing Club" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=64)
        elif "Air Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=63)
        elif "Pinewood Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=129)
        elif "Elstree Studios" in venue_name:
            venue_id = VenueItem.django_model.objects.get(id=128)
        else:
            venue_id = VenueItem.django_model.objects.get(id=0)

        slug = slugify(title)
        image_urls = response.xpath('//div[@class="image"]/img/@src').extract_first()
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
