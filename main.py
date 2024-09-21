import asyncio
import json
from datetime import datetime

from dotenv import load_dotenv

from aidy import pull_from_aidy
from spacenews import pull_from_spacenews
from twitter import pull_from_twitter
from vestaboard import push_to_vestaboard

load_dotenv()

CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')

PERSISTED_DATA = json.load(open('./data.json'))

if PERSISTED_DATA["date"] != CURRENT_DATE:
    ...


def execute_steps():
    if len(PERSISTED_DATA["aidy_queue"]) > 0:
        # push_to_vestaboard(PERSISTED_DATA["aidy_queue"][0])
        # PERSISTED_DATA["aidy_queue"].pop(0)
        # return
        ...
    aidy_queue = pull_from_aidy(already_pushed=PERSISTED_DATA["aidy_ids"])

    if len(aidy_queue) > 0:
        PERSISTED_DATA["aidy_queue"] = aidy_queue
#         push_to_vestaboard(PERSISTED_DATA["aidy_queue"][0])
#         PERSISTED_DATA["aidy_queue"].pop(0)
#         return
        ...
    if len(PERSISTED_DATA["spacenews_queue"]) > 0:
#         push_to_vestaboard(PERSISTED_DATA["spacenews_queue"][0])
#         PERSISTED_DATA["spacenews_queue"].pop(0)
#         return
        ...
    spacenews_queue = pull_from_spacenews(already_pushed=PERSISTED_DATA["spacenews_ids"])

    if len(spacenews_queue) > 0:
        PERSISTED_DATA["spacenews_queue"] = spacenews_queue
#         push_to_vestaboard(PERSISTED_DATA["spacenews_queue"][0])
#         PERSISTED_DATA["spacenews_queue"].pop(0)
#         return
        ...
    if len(PERSISTED_DATA["twitter_queue"]) > 0:
#         push_to_vestaboard(PERSISTED_DATA["twitter_queue"][0])
#         PERSISTED_DATA["twitter_queue"].pop(0)
#         return
        ...
    twitter_queue = asyncio.run(pull_from_twitter(already_pushed=PERSISTED_DATA["twitter_ids"]))

    if len(twitter_queue) > 0:
        PERSISTED_DATA["twitter_queue"] = twitter_queue
#         push_to_vestaboard(PERSISTED_DATA["twitter_queue"][0])
#         PERSISTED_DATA["twitter_queue"].pop(0)
#         return
        ...
    print(PERSISTED_DATA)


if __name__ == "__main__":
    execute_steps()
