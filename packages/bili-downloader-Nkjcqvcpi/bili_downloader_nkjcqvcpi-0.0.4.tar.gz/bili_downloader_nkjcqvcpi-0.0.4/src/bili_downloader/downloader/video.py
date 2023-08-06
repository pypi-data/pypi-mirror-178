import os.path
import time
import random
import logging
import requests

from .._base_dler import BaseDler
from ..converter import merge as _merge

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class VideoDler(BaseDler):
    VIDEO_API = 'https://api.bilibili.com/x/player/playurl'
    page_param = {'cid': None, 'fnval': 16}

    def __init__(self, sessdata, dl_path=None, cfg_path=None, merge=True, video=True, audio=True, dry_run=False):
        self.merge = merge
        self.video = video
        self.audio = audio
        super().__init__(sessdata=sessdata, dl_path=dl_path, cfg_path=cfg_path, mode='video', dry_run=dry_run)

    def __call__(self, *args, **kwargs):
        items = self.parser(*args, **kwargs)
        videos = self.download_videos(items['video'], video=self.video, audio=self.audio)
        if self.merge and not self.dry_run:
            files = [_merge(os.path.join(self.dl_path, f'{video}_{page}.mov'), video=info['video'], audio=info['audio'])
                     for video, pages in videos.items() for page, info in pages.items()]
            return files
        return videos
    
    def download_videos(self, items, video=True, audio=True):
        files = {}
        for v_info in items:
            self.page_param.update({'bvid': v_info['bvid']})
            logging.info('Downloading Video: %s', v_info['title'])
            files[v_info['bvid']] = {'cover': self._download(v_info['pic'])}
            for page in v_info['pages']:
                logging.info('\tDownloading Page: %s', page['part'])
                self.page_param['cid'] = page['cid']
                p_info = requests.get(self.VIDEO_API, params=self.page_param, cookies=self.cookie).json()['data']
                staffs = {'UP主': [staff['name'] for staff in v_info['staff'] if staff['title'] == 'UP主'][0],
                          '演唱': [staff['name'] for staff in v_info['staff'] if staff['title'] == '演唱']}
                file = {'metadata': {'\xa9nam': page['part'], '\xa9alb': v_info['title'], 'aART': staffs['UP主'],
                                     '\xa9ART': ';'.join([staffs['UP主']] + staffs['演唱']), '\xa9cmt': v_info['desc'],
                                     '\xa9day': time.localtime(v_info['pubdate']).tm_year, 'desc': ''}}
                if video:
                    file['video'] = self.download(p_info['dash']['video'][0]['baseUrl'])
                    time.sleep(random.random())
                if audio:
                    file['audio'] = self.download(p_info['data']['audio'][0]['baseUrl'])
                    time.sleep(random.random())
                files[v_info['title']][page['part']] = file
        return files
