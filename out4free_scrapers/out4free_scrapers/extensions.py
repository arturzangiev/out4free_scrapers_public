from scrapy import signals
import smtplib


class StatsReporter(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_closed(self, spider):

        if self.stats.get_value('response_received_count') == 1:

            msg = "\r\n".join(["Subject: Broken spider " + spider.name,
                               "From: test@test.com",
                               "To: test@test.com",
                               "\nThe system is not collecting links as the response count is 1"])

            server = smtplib.SMTP('smtp.yandex.ru', 587)
            server.ehlo()
            server.starttls()
            server.login("test@test.com", "")
            server.sendmail("test@test.com", "test@test.com", msg)

        elif self.stats.get_value('log_count/ERROR') is not None and self.stats.get_value('log_count/ERROR') > 0:

            msg = "\r\n".join(["Subject: Errors spider " + spider.name,
                               "From: test@test.com",
                               "To: test@test.com",
                               "\nThe number of errors is " + str(self.stats.get_value('log_count/ERROR'))])

            server = smtplib.SMTP('smtp.yandex.ru', 587)
            server.ehlo()
            server.starttls()
            server.login("test@test.com", "")
            server.sendmail("test@test.com", "test@test.com", msg)
