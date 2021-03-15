import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from credobank.items import Article
import requests
import json


class CredobankSpider(scrapy.Spider):
    name = 'credobank'
    start_urls = ['https://credobank.ge/wp-json/mediaroom/v2/mediaroom?month=all&year=all&page=1&lang=en']

    def parse(self, response):
        page = 1
        response = json.loads(requests.get(f"https://credobank.ge/wp-json/mediaroom/v2/mediaroom?month=all&year=all"
                                           f"&page={page}&lang=en").text)
        pages = response['max_pages']
        while page <= pages:
            response = json.loads(requests.get(f"https://credobank.ge/wp-json/mediaroom/v2/mediaroom?month=all&year=all"
                                               f"&page={page}&lang=en").text)
            page += 1
            for post in response['posts']:
                item = ItemLoader(Article())
                item.default_output_processor = TakeFirst()

                if 'title' in post.keys():
                    title = post['title']
                else:
                    title = ''

                if 'acf' in post.keys():
                    date = post['acf']['date']
                else:
                    date = ''

                if 'acf' in post.keys():
                    content = post['acf']['short_description']
                else:
                    content = ''

                if 'permalink' in post.keys():
                    link = post['permalink']
                else:
                    link = ''

                item.add_value('title', title)
                item.add_value('date', date)
                item.add_value('link', link)
                item.add_value('content', content)

                yield item.load_item()

