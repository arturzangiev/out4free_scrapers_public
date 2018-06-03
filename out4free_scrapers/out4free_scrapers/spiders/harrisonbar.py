# -*- coding: utf-8 -*-
import scrapy
from ..items import EventItem, CatItem, VenueItem
from slugify import slugify


class HarrisonbarSpider(scrapy.Spider):
    name = "harrisonbar"
    allowed_domains = ["harrisonbar.co.uk"]
    start_urls = ['http://harrisonbar.co.uk/full-calendar/']

    def parse(self, response):
        urls = response.xpath('//div[@class="ai1ec-event-title"]/div/a[@class="ai1ec-load-event"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

    def individual_page(self, response):
        title = response.xpath('//h2[@class="entry-title fusion-post-title"]/text()').extract_first()
        description = response.xpath('//div[@class="post-content"]//p/text()').extract()
        description = " ".join(description)
        price = response.xpath('//div[@class="ai1ec-field-value ai1ec-col-sm-9"]/text()').extract_first().strip()
        start_datetime = response.xpath('//div[@class="ai1ec-hidden dt-start"]/text()').extract_first()
        category_id = CatItem.django_model.objects.get(id=1)
        venue_id = VenueItem.django_model.objects.get(id=30)
        slug = slugify(title)
        image_urls = response.xpath('//div[@class="ai1ec-event-avatar timely timely alignleft ai1ec-post_thumbnail ai1ec-portrait"]/img/@src').extract_first()
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
