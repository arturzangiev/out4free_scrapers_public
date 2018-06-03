# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class SouthbankSpider(scrapy.Spider):
    name = "southbankcentre"
    allowed_domains = ["southbankcentre.co.uk"]
    start_urls = ['https://www.southbankcentre.co.uk/whats-on?field_api_event_free=1&free=1']

    def parse(self, response):
        urls = response.xpath('//div[@class="c-event-listing-title"]/a/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//div[@class="panel-pane pane-custom pane-1"]/h1/text()').extract_first().strip()
        description = response.xpath('//div[@class="field__item even"]/p/text()').extract_first()
        price = response.xpath('//div[@class="c-collapsible-block__subtitle"]/text()').extract()[-1].strip()
        date = response.xpath('//div[@class="c-collapsible-block__subtitle"]/text()').extract()[0].strip()
        regex_date = re.sub(r"^(\d+ \w{3} \d+)( - \d+ \w{3} \d+)?$", r"\1", date)
        time = response.xpath('//div[@class="c-performance-details__time"]/text()').extract()[0]
        start_datetime = regex_date + ' ' + time
        category_id = CatItem.django_model.objects.get(id=3)
        venue_id = VenueItem.django_model.objects.get(id=22)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="content"]/img/@src').extract_first()
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
