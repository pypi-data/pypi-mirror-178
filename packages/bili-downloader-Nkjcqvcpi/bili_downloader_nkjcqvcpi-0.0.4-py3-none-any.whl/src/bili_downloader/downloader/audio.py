import logging
import time
import random

import requests

from .._base_dler import BaseDler
from ..converter import apple_music

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AudioDler(BaseDler):
    AUDIO_API = 'https://api.bilibili.com/audio/music-service-c/url'

    def __init__(self, sessdata, dl_path=None, cfg_path=None, music=True, dry_run=False):
        self.apple_music = music
        super().__init__(sessdata=sessdata, dl_path=dl_path, cfg_path=cfg_path, mode='audio', dry_run=dry_run)

    def __call__(self, *args, **kwargs):
        items = self.parser(*args, **kwargs)
        audios = self.download_audios(items['audio'])
        if self.apple_music and not self.dry_run:
            files = [apple_music(audio=audio['audio'], music_path=self.dl_path, metadata=audio['metadata'],
                                 lyric=audio['lyric'], cover=audio['cover']) for aid, audio in audios.items()]
            return files
        return audios

    def download_audios(self, items):
        files = {}
        for aid in items:
            param = {'songid': aid['id'], 'quality': 3, 'privilege': 2, 'mid': '', 'platform': ''}
            a_info = requests.get(self.AUDIO_API, params=param, cookies=self.cookie).json()['data']
            logging.info('Downloading Audio:', aid['title'])
            files[aid['id']] = {'cover': self._download(aid['cover']), 'lyric': self._download(aid['lyric']),
                                'audio': self.download(a_info['data']),
                                'metadata': {'\xa9nam': aid['title'], '\xa9alb': aid['title'], '\xa9ART': aid['uname'],
                                             'aART': aid['uname'], '\xa9day': time.localtime(aid['passtime']).tm_year,
                                             '\xa9cmt': aid['intro']}, 'desc': ''}
            time.sleep(random.random())
        return files
