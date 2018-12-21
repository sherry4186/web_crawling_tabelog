# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter


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
