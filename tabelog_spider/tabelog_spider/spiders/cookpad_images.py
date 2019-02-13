import os
import scrapy
import pandas as pd


class CookpadImageSpider(scrapy.Spider):
    name = "cookpadimage"

    def start_requests(self):
        urls = []

        df = pd.read_csv(os.path.join('spiders', 'source_data', 'cookpad_id.csv'), names=['cookpad_id'])

        cookpad_ids = df['cookpad_id'].tolist()
        for cookpad_id in cookpad_ids:
            url = f'https://cookpad.com/recipe/{cookpad_id}'
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        recipe_image_url = response.css("div.clearfix img::attr(data-large-photo)").extract_first()
        if recipe_image_url is not None:
            recipe_id = recipe_image_url.split('/')[4]

            yield {
                'recipe_id': recipe_id,
                'recipe_image_url': recipe_image_url}
