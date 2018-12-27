import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd

from spiders.tabelog_review import TabelogSpider


def start_crawling():

    process = CrawlerProcess(get_project_settings())
    process.crawl(TabelogSpider)
    process.start()


def return_shopid():
    """get shop_ids from "restaurants.txt" and output to a csv_file (which will be used by spider)
    """
    shopid_list = []

    with open('spiders/restaurants_test.txt', "r") as f:
        lines = f.readlines()
    for line in lines:
        j = json.loads(line)
        shopid_list.append(j['id'])

    df = pd.DataFrame(shopid_list, columns=['shop_id'])
    df.to_csv('spiders/tabelog_shopid.csv', index=False)


def process_output(result_file):
    df = pd.read_csv(result_file)
    df['shop_id'] = df['shop_id'].str.slice(20, -1)

    output_filename = result_file.replace('.csv', '') + '_processed.csv'
    df.to_csv(output_filename, index=False)


return_shopid()
start_crawling()
process_output(result_file='tabelog.csv')
