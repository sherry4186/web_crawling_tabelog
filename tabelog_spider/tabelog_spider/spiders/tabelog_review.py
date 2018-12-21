from datetime import datetime
from dateutil.relativedelta import relativedelta
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import pandas as pd
from twisted.internet import reactor


class TabelogSpider(scrapy.Spider):
    name = "tabelog"

    month_now = datetime.now()

    def return_start_urls(self):
        df = pd.read_csv('spiders/tabelog_shopid.csv', names=['shop_id'])
        return df['shop_id'].tolist()

    def start_requests(self):
        urls = []

        shop_ids = self.return_start_urls()
        for shop_id in shop_ids:
            url = f'https://tabelog.com/{shop_id}/dtlrvwlst/COND-0/smp1/D-visit/?lc=0&rvw_part=all'
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # get shop_id
        # for example: "https://tabelog.com/tokyo/A1304/A130401/13045287/"
        shop_id = response.css("div.rdheader-rstname a::attr(href)").extract_first()

        crawl_next_page_flag = True

        for kuchikomi in response.css("div.js-rvw-item-wrapper"):
            review_date = kuchikomi.css('div.rvw-item__date p::text').extract_first().strip()[:-2]

            # this review is written in this month or last month
            if ((review_date == (self.month_now - relativedelta(months=1)).strftime("%Y/%m")) or (review_date == self.month_now.strftime("%Y/%m"))):
                yield {
                    'shop_id': shop_id,
                    'review_date': review_date}
            else:
                crawl_next_page_flag = False
                break

        if crawl_next_page_flag:
            next_page = response.css('li.c-pagination__item a::attr(href)')[-1]
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
