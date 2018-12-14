from datetime import datetime
from dateutil.relativedelta import relativedelta
import scrapy


class TabelogSpider(scrapy.Spider):
    name = "tabelog"

    month_now = datetime.now()

    def start_requests(self):
        urls = [
            'https://tabelog.com/tokyo/A1301/A130101/13044694/dtlrvwlst/COND-0/smp1/D-visit/?lc=0&rvw_part=all',
            'https://tabelog.com/tokyo/A1308/A130802/13015251/dtlrvwlst/COND-0/smp1/D-visit/?lc=0&rvw_part=all'
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for kuchikomi in response.css("div.js-rvw-item-wrapper"):
            review_date = kuchikomi.css('div.rvw-item__date p::text').extract_first().strip()[:-2]

            # this review is written in this month or last month
            if (review_date == (self.month_now - relativedelta(months=1)).strftime("%Y/%m")) or (review_date == self.month_now.strftime("%Y/%m")):
                yield {
                    'review_date': review_date}
            else:
                break
