import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
import requests

load_dotenv()

AIDY_API_URL = os.environ.get('AIDY_API_URL') + "/search-bills"

params = {
    'query': 'Space Policy',
    'policies': '',
    'chambers': '',
    'doc_type': 'bill',
    'start_date': datetime.now().strftime('%Y-%m-%d'),
}


def pull_from_aidy(already_pushed: list[int]) -> List[str]:
    try:
        aidy_queue = []
        response = requests.get(AIDY_API_URL, params=params)
        response.raise_for_status()
        response = response.json()

        space_bills = response['objects']
        for space_bill in space_bills:
            if space_bill['id'] in already_pushed:
                continue
            already_pushed.append(space_bill['id'])
            actions = space_bill['actions']
            actions.sort(key=lambda x: datetime.strptime(x['action_date'], '%Y-%m-%d'))
            message = f"{response['bill_type']} {response['bill_number']} {actions[0]['actionCode'].split(' ')[0]}: {response['title']}"
            aidy_queue.append(message)
        return aidy_queue
    except Exception as e:  # NOQA
        print(e)
        return []
