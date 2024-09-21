from typing import List

import requests
import xml.etree.ElementTree as ET  # NOQA

# URL of the SpaceNews RSS feed
RSS_FEED_URL = "https://spacenews.com/feed/"


def pull_from_spacenews(already_pushed: List[int]) -> List[str]:
    try:
        spacenews_queue = []
        response = requests.get(RSS_FEED_URL)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        spacenews_items = root.findall('.//item')
        # print(spacenews_items)
        namespaces = {
            'wp': 'com-wordpress:feed-additions:1'
        }
        for spacenews_item in spacenews_items:
            title = spacenews_item.find('./title').text
            post_id = int(spacenews_item.find('./wp:post-id', namespaces).text)
            if post_id in already_pushed:
                continue
            spacenews_queue.append(title)
            already_pushed.append(post_id)
        return spacenews_queue
    except Exception as e:
        print(e)
        return []
