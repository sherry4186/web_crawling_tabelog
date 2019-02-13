import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd

from spiders.tabelog_review import TabelogSpider
from spiders.cookpad_images import CookpadImageSpider


def start_crawling(spider):

    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
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


def process_output(input_file, suffix):
    """change shop_ids: 
       'https://tabelog.com/tokyo/A1304/A130401/13045287/' → 'tokyo/A1304/A130401/13045287'

    Args:
        input_file: origin file (like 'tabelog.csv')
        suffix:     suffix (like '_processed.csv' so that output file is 'tabelog_processed.csv')

    """
    df = pd.read_csv(input_file)
    df['shop_id'] = df['shop_id'].str.slice(20, -1)

    output_filename = input_file.replace('.csv', '') + suffix
    df.to_csv(output_filename, index=False)


def main_tabelog_review_spider():
    return_shopid()
    start_crawling(spider=TabelogSpider)
    process_output(input_file='tabelog.csv', suffix='_processed.csv')


def main_cookpad_recipe_image_spider():
    start_crawling(spider=CookpadImageSpider)


main_cookpad_recipe_image_spider()
