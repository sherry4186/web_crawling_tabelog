import os
import pandas as pd
import requests


def image_download(info):
    """download images

    Args:
        info: (shop_id,image_url) pair

    """
    image_file = 'image/' + info[0].replace('/', '_') + '.jpg'
    image_url = info[1]

    r = requests.get(image_url)
    with open(image_file, 'wb') as f:
        f.write(r.content)
    return True


def start_crawling(image_data_file, download_folder='image/'):
    """get (shop_id,image_url) pair from "data/image_data_test.csv" and download images
    """

    # image folder
    os.makedirs(download_folder, exist_ok=True)

    df = pd.read_csv(image_data_file)

    result = list(map(image_download, list(zip(df['id'], df['image_url']))))


start_crawling(image_data_file="data/image_data_test.csv")
