from django.db import models
from django.conf import settings
from datetime import datetime
from collections import defaultdict, OrderedDict
import collections, json


def load_news():
    with open(settings.NEWS_JSON_PATH, 'r') as file_read:
        data = json.load(file_read)
    return data

def add_news(news):
    curr_news = load_news()
    curr_news.append(news)
    with open(settings.NEWS_JSON_PATH, 'w') as file_write:
        json.dump(curr_news, file_write)

def get_news_sorted(query):
    news_content = load_news()
    for item in news_content:
        item['created'] = item['created'][:10]
    grouped = collections.defaultdict(list)
    if query:
        for item in news_content:
            if query.lower() in item.get('title').lower():
                grouped[item['created']].append(item)
    else:
        for item in news_content:
            grouped[item['created']].append(item)
    return OrderedDict(sorted(grouped.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True))