import json
import logging

import requests
from .._base_dler import BaseDler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


MAN_API = 'https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail'
INDEX_API = 'https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex'
TOKEN_API = 'https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken'


class MangaDler(BaseDler):
    def __init__(self):
        self.HEADER['Content-Type'] = 'application/json'

    def download_manga(self, comic_id, tmpdir, cookie):
        mg = requests.post(MAN_API, data=json.dumps({"comicId": comic_id}), headers=self.HEADER, params={'device': 'pc'}).json()
        manga = [download_episode(ep['id'], tmpdir, cookie) for ep in mg['ep_list']]
        return manga

    def download_episode(self, ep_id, tmpdir, cookie):
        cookie['SESSDATA'] = 'e36f978d%2C1672999949%2C1f56d*71'
        idx = requests.post(INDEX_API, data=json.dumps({"ep_id": ep_id}), cookies=cookie, headers=HEADER,
                            params={'device': 'pc'}).json()

        urls = '["' + '","'.join([f'https://i0.hdslb.com{img["path"]}' for img in idx['data']['images']]) + '"]'

        req = requests.post(TOKEN_API, data=json.dumps({"urls": urls}), cookies=cookie, headers=HEADER).json()
        imgs = [_download(img['url'] + '?token=' + img['token'], tmpdir) for img in req['data']]
        return imgs
