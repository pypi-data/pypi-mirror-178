import requests
import json

from .._base_dler import BaseDler

HEADER['Content-Type'] = 'application/json'
BUY_API = 'https://manga.bilibili.com/twirp/user.v1.User/GetAutoBuyComics'


def get_comics(cookie) -> []:
    comics = []
    cookie['SESSDATA'] = 'e36f978d%2C1672999949%2C1f56d*71'
    data = {"page_num": 1,"page_size": 100}
    while True:
        req = requests.post(BUY_API, data=json.dumps(data), headers=HEADER, cookies=cookie).json()
        comics.extend(req['data'])
        data["page_num"] += 1
        if len(req['data']) < 1:
            break
    return comics
