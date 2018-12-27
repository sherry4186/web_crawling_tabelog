from multiprocessing.dummy import Pool as ThreadPool
import os
import pandas as pd
import requests
from time import sleep


def image_download(info):
    """download images

    Args:
        info: (shop_id,image_url) pair

    """
    image_file = 'image/' + info[0].replace('/', '_') + '.jpg'
    image_url = info[1]

    sleep(3)
    r = requests.get(image_url)
    with open(image_file, 'wb') as f:
        f.write(r.content)
    return True


def start_crawling(image_data_file, download_folder='image/'):
    """get (shop_id,image_url) pair from "data/image_data_test.csv" and download images
    """

    # image folder
    os.makedirs(download_folder, exist_ok=True)

    pool = ThreadPool()

    df = pd.read_csv(image_data_file)

    '''
    if download 30 times, it'll spend:
        map function：94.9s
        Pool：25.2s
        ThreadPool：26.5s

    if download 120 times, it'll spend:
        Pool：103.9s
        ThreadPool：99.6s

    so use ThreadPool
    '''
    results = pool.map(image_download, list(zip(df['id'], df['image_url'])))

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()


start_crawling(image_data_file="data/image_data_test.csv")
