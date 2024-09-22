import asyncio
import json
from datetime import datetime

from dotenv import load_dotenv

from aidy import pull_from_aidy
from spacenews import pull_from_spacenews
from supercluster import pull_from_supercluster
from twitter import pull_from_twitter
from vestaboard import push_to_vestaboard
from git import Repo

load_dotenv()

CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')


def create_persisted_data():
    return {
        "date": CURRENT_DATE,
        "aidy_ids": [],
        "aidy_queue": [],
        "supercluster_ids": [],
        "supercluster_queue": [],
        "spacenews_ids": [],
        "spacenews_queue": [],
        "twitter_ids": [],
        "twitter_queue": []
    }


try:
    PERSISTED_DATA = json.load(open('./data.json'))
except Exception as e:
    PERSISTED_DATA = create_persisted_data()

if PERSISTED_DATA["date"] != CURRENT_DATE:
    PERSISTED_DATA = create_persisted_data()


def execute_steps():
    if len(PERSISTED_DATA["aidy_queue"]) > 0:
        push_to_vestaboard(PERSISTED_DATA["aidy_queue"][0], source="aidy")
        PERSISTED_DATA["aidy_queue"].pop(0)
        return
        ...

    aidy_queue = pull_from_aidy(already_pushed=PERSISTED_DATA["aidy_ids"])

    if len(aidy_queue) > 0:
        PERSISTED_DATA["aidy_queue"] = aidy_queue
        push_to_vestaboard(PERSISTED_DATA["aidy_queue"][0], source="aidy")
        PERSISTED_DATA["aidy_queue"].pop(0)
        return
        ...

    if len(PERSISTED_DATA["supercluster_queue"]) > 0:
        push_to_vestaboard(PERSISTED_DATA["supercluster_queue"][0], source="supercluster")
        PERSISTED_DATA["supercluster_queue"].pop(0)
        return
        ...

    supercluster_queue = pull_from_supercluster(already_pushed=PERSISTED_DATA["supercluster_ids"])

    if len(supercluster_queue) > 0:
        PERSISTED_DATA["supercluster_queue"] = supercluster_queue
        push_to_vestaboard(PERSISTED_DATA["supercluster_queue"][0], source="supercluster")
        PERSISTED_DATA["supercluster_queue"].pop(0)
        return
        ...

    if len(PERSISTED_DATA["spacenews_queue"]) > 0:
        push_to_vestaboard(PERSISTED_DATA["spacenews_queue"][0], source="spacenews")
        PERSISTED_DATA["spacenews_queue"].pop(0)
        return
        ...
    spacenews_queue = pull_from_spacenews(already_pushed=PERSISTED_DATA["spacenews_ids"])

    if len(spacenews_queue) > 0:
        PERSISTED_DATA["spacenews_queue"] = spacenews_queue
        push_to_vestaboard(PERSISTED_DATA["spacenews_queue"][0], source="spacenews")
        PERSISTED_DATA["spacenews_queue"].pop(0)
        return
        ...

    if len(PERSISTED_DATA["twitter_queue"]) > 0:
        push_to_vestaboard(PERSISTED_DATA["twitter_queue"][0], "twitter")
        PERSISTED_DATA["twitter_queue"].pop(0)
        return
        ...

    twitter_queue = asyncio.run(pull_from_twitter(already_pushed=PERSISTED_DATA["twitter_ids"]))

    if len(twitter_queue) > 0:
        PERSISTED_DATA["twitter_queue"] = twitter_queue
        push_to_vestaboard(PERSISTED_DATA["twitter_queue"][0], "twitter")
        PERSISTED_DATA["twitter_queue"].pop(0)
        return
        ...

    print(PERSISTED_DATA)


if __name__ == "__main__":
    execute_steps()
    # repo = Repo("./")
    json.dump(PERSISTED_DATA, open('./data.json', 'w'))
    # repo.index.add(['./data.json'])
    # repo.index.commit("Updated Persistent data")
    # origin = repo.remote(name='origin')
    # origin.push()
