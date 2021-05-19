from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from app.core.config import settings
from app.workers.worker import celery_app

ATTEMPTS = 3

client = MongoClient(settings.MONGO_URI)
db = client.feed


@celery_app.task()
def update_feeds():
    feeds = db["feeds"].find({"retries": {'$lt': ATTEMPTS}})
    for feed in feeds:
        celery_app.send_task('update_feed', args=[feed.get("_id")])
    return True


@celery_app.task(name='update_feed')
def update_feed(feed_id: str):
    feed = db["feeds"].find_one({"_id": feed_id})
    retries = 0
    r = requests.get(feed.get('url'))
    soup = BeautifulSoup(r.content, features='xml')
    try:
        channel = soup.find('channel')
        fetched = {
            'title': channel.find('title').text if channel.find('title') else None,
            'link': channel.find('link').text if channel.find('link') else None,
            'description': channel.find('description').text if channel.find('description') else None,
            'retries': 0
        }
        feed = feed | fetched
    except AttributeError:
        retries += feed.get('retries', 0) + 1
        feed = feed | {'retries': retries}
    db["feeds"].update_one({"_id": feed_id}, {"$set": feed})
    return True


@celery_app.task()
def update_feed_item(url: str = None):
    query = {'updates_enabled': True}
    if url:
        query.update({'url': url})
    feeds = db["feeds"].find(query)
    for feed in feeds:
        url = feed.get('url')
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='xml')
        items = soup.findAll('item')
        for a in items:
            title = a.find('title').text if a.find('title') else None
            link = a.find('link').text if a.find('link') else None
            summary = a.find('description').text if a.find('description') else None
            author = a.find('author').text if a.find('author') else None
            entry = {
                'url': url,
                'title': title,
                'link': link,
                'author': author,
                'summary': summary,
                'read': False,
                'last_updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
            }
            has_entry = db["entries"].find_one({"link": link})
            if not has_entry:
                db["entries"].insert_one(entry)
    return True


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5*60, update_feeds.s(), name='retry every 5 minutes')
    sender.add_periodic_task(60, update_feed_item.s(), name='update every 60 seconds')
