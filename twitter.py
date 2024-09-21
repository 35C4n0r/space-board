import asyncio
import os
from typing import List
import dotenv
from twikit.guest import GuestClient

client = GuestClient()
dotenv.load_dotenv()

TWITTER_USERS: List[str] = os.getenv('TWITTER_USERS').split(",")


async def pull_from_twitter(already_pushed: List[int]):
    twitter_queue = []
    await client.activate()
    # Get user by screen name
    for user in TWITTER_USERS:

        user = await client.get_user_by_screen_name(screen_name=user)
        user_tweets = await client.get_user_tweets(user_id=user.id, count=10)
        print(user.screen_name, len(user_tweets))
        for tweet in user_tweets:
            if tweet.id in already_pushed:
                continue
            twitter_queue.append(tweet.text)
            already_pushed.append(int(tweet.id))
    return twitter_queue
