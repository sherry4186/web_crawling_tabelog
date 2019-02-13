# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline


class TabelogSpiderExportPipeline(object):
    """Get 'EXPORT_URI' from settings.py, then write items to 'EXPORT_URI' (which is a csv file).
       (create this PipelineClass to overwrite export_file when that file exists)

    Attributes:
        uri: 'EXPORT_URI' (which is a csv file) from settings.py

    """

    def __init__(self, uri):
        self.uri = uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('EXPORT_URI'),
        )

    def open_spider(self, spider):
        self.export_file = open(self.uri, 'wb')
        self.exporter = CsvItemExporter(self.export_file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.export_file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class CookpadImageSpiderExportPipeline(ImagesPipeline):
    """ Get recipe's id and image, then download the image and name the image_file like: id.jpg (for example: 3398.jpg)

    """

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['recipe_image_url'], meta={'item': item})

    def file_path(self, request, response=None, info=None):
        """ Rename image_file name (default name is random string)

        """
        item = request.meta['item']
        file_name = item['recipe_id'] + '.jpg'
        return file_name
