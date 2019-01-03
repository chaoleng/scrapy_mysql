import time
import os
# from scrapy import cmdline
# cmdline.execute('scrapy crawl douban_spider'.split())
while True:
    os.system("scrapy crawl douban_spider")
    time.sleep(3600) 