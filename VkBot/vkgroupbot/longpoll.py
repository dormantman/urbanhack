import json
import requests
from .exceptions import LongPoolFailedError


class LongPollApi:
    def __init__(self, server: str, key: str, ts: str, wait=1):
        self.server = server
        self.key = key
        self.ts = ts
        self.wait = 1


    def make_url(self):
        return f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait={self.wait}'


    def get(self):
        r = requests.get(self.make_url())
        if r.status_code == 200:
            response = json.loads(r.text)  # type: dict

            if response.get('failed'):
                raise LongPoolFailedError(response['failed'])

            self.ts = response['ts']
            return response
