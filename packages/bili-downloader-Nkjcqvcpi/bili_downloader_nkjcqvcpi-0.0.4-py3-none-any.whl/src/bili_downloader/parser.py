import math
import random
import time
import json
import logging
from urllib.parse import urlparse

import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Parser:
    API = {'nav': 'https://api.bilibili.com/x/space/navnum',
           'video': 'https://api.bilibili.com/x/space/arc/search',
           'audio': 'https://api.bilibili.com/audio/music-service/web/song/upper',
           'album': 'https://api.bilibili.com/x/dynamic/feed/draw/doc_list',
           'dynamic': 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail'}
    AUDIO_API = 'https://api.bilibili.com/audio/music-service-c/web/song/info'
    INFO_API = 'https://api.bilibili.com/x/web-interface/view'
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                            'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'}
    param = {'video': {'mid': int, 'ps': 50, 'tid': 0, 'pn': 1, 'keyword': '', 'order': 'pubdate',
                       'order_avoid': 'true', 'jsonp': 'jsonp'},
             'audio': {'uid': int, 'pn': 1, 'ps': 10000, 'order': 1, 'jsonp': 'jsonp'},
             'album': {'uid': int, 'page_num': 0, 'page_size': 2147483647, 'biz': 'all', 'jsonp': 'jsonp'}}

    def __init__(self, sessdata, mode='up'):
        self.cookie = {'SESSDATA': sessdata}
        if mode == 'up':
            self.mode = ['video', 'audio', 'album', 'dynamic']
        elif mode == 'music':
            self.mode = ['video', 'audio']
        else:
            self.mode = mode

    def __call__(self, *args, **kwargs) -> dict:
        """

        :param args: [url], url, (url,), [uid], uid
        :param kwargs:
        :return:
        """
        self.results = {k: [] for k in self.mode}
        for arg in args:
            if isinstance(arg, (str, int)):
                arg = [arg]
            for ar in arg:
                if isinstance(ar, int):
                    self.uid_parser(arg)
                elif isinstance(ar, str):
                    url = urlparse(ar)
                    if url.scheme:
                        self.urlparser(url)
                    elif url.path:
                        self.uid_parser(arg)
                else:
                    raise SyntaxWarning
        return self.results

    def urlparser(self, url):
        logging.debug('urlparser')
        _id = url.path.split('/')[-1]
        if _id.startswith('BV') and 'video' in self.mode:
            param = {'bvid': _id}
            self.results['video'].append(requests.get(self.INFO_API, params=param, cookies=self.cookie).json()['data'])
        elif _id.startswith('av') and 'video' in self.mode:
            param = {'avid': _id}
            self.results['video'].append(requests.get(self.INFO_API, params=param, cookies=self.cookie).json()['data'])
        elif _id.startswith('au') and 'audio' in self.mode:
            self.results['audio'].append(requests.get(self.AUDIO_API, params={'sid': _id}).json()['data'])
        elif _id.isdigit() and 'dynamic' in self.mode:
            card = requests.get(self.API['dynamic'], params={'dynamic_id': _id}).json()['data']['card']['card']
            self.results['dynamic'].append(json.loads(card)['item'])
        else:
            raise SyntaxWarning

    def uid_parser(self, uid):
        logging.debug('_uid_parser')
        nav = requests.get(self.API['nav'], headers=self.header, params={'mid': uid}).json()
        if 'video' in self.mode:
            self.param['video']['mid'] = uid
            self.results['video'].extend(self.get_list(mode='video', num=nav['data']['video']))
        if 'audio' in self.mode:
            self.param['audio']['uid'] = uid
            self.results['audio'].extend(self.get_list(mode='audio', num=nav['data']['audio']))
        if 'album' in self.mode:
            self.param['album']['uid'] = uid
            self.results['album'].extend(self.get_list(mode='album', num=nav['data']['album']))

    def get_list(self, mode, num):
        li = []
        num = math.ceil(num / self.param[mode]['page_size' if mode == 'album' else 'ps'])
        for pn in range(1, num + 1):
            self.param[mode]['pn'] = pn
            req = requests.get(self.API[mode], headers=self.header, params=self.param[mode]).json()
            if mode == 'video':
                for v in req['data']['list']['vlist'][:2]:
                    li.append(requests.get(self.INFO_API, params={'bvid': v['bvid']}, cookies=self.cookie).json()['data'])
                    time.sleep(random.random())
            elif mode == 'audio':
                li.extend(req['data']['data'])
            elif mode == 'album':
                li.extend(req['data']['items'])
            time.sleep(random.random())
        return li


if __name__ == '__main__':
    alurl = 'https://t.bilibili.com/730581161356558377?spm_id_from=333.999.0.0'
    aurl = 'https://www.bilibili.com/audio/au2515961?type=3&spm_id_from=333.999.0.0'
    vurl = 'https://www.bilibili.com/video/BV16R4y1M7XC?from=search&seid=772507573660196375&spm_id_from=333.337.0.0'
    # Up(uid=353837540)
    p = Parser(sessdata='b4f0af61%2C1659237450%2C8f896*21', mode='up')
    p(353837540)
    i = 0
