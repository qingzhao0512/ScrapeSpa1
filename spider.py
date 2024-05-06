'''
Author: qingzhao0512 qingzhao0512@gmail.com
Date: 2024-05-06 14:39:27
LastEditors: qingzhao0512 qingzhao0512@gmail.com
LastEditTime: 2024-05-06 15:33:52
FilePath: \ScrapeSpa1\spider.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests
import logging
import json
from os import makedirs
from os.path import exists


""" # 查看这个URL和最初的是否有不同
url = 'https://spa1.scrape.center/'
html = requests.get(url).text
print(html)

url = 'https://ssr1.scrape.center/'
html = requests.get(url).text
print(html) """



logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 定义列表页的URL
INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'
# 定义详情页的URL
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'
LIMIT = 10
TOTAL_PAGE = 10
RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


def scrape_api(url):                            # 这个方法专门用来处理JSON接口
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()              # 最后response调用的是JSON方法，返回的是JSON格式的数据
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


def scrape_detail(id):                        # 定义详情页的爬取逻辑
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)


def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)                    # 调用scrape_index方法，获取列表页的JSON数据
        for item in index_data.get('results'):             # 遍历列表页的JSON数据
            id = item.get('id')
            detail_data = scrape_detail(id)                # 调用scrape_detail方法，获取详情页的JSON数据
            logging.info('detail data %s', detail_data)
            save_data(detail_data)


if __name__ == '__main__':
    main()
