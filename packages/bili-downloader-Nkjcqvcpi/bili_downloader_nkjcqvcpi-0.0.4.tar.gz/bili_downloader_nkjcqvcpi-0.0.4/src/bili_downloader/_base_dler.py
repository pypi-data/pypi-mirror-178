import os
import sqlite3
import tempfile
import shutil
from pathlib import Path
from urllib.parse import urlparse
from configparser import ConfigParser

import requests
from tqdm.auto import tqdm

from .parser import Parser


class BaseDler:
    HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                            'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
              'Referer': 'https://www.bilibili.com'}

    def __init__(self, sessdata: str, dl_path=None, cfg_path=None, mode='', dry_run=False):
        """

        :param sessdata: Bilibili Login Cookie
        :param dl_path:
        :param cfg_path:
        """
        self.parser = Parser(sessdata=sessdata, mode=mode)
        self.cookie = {'SESSDATA': sessdata}
        self.dl_path = Path(dl_path) if dl_path else Path.cwd()
        self.cfg, self.cfg_path = self.init_config(cfg_path)
        self.tmpdir = tempfile.TemporaryDirectory()
        self.dry_run = dry_run
        self.db = self.init_history()

    def init_history(self):
        db = sqlite3.connect(os.path.join(self.cfg_path, 'history.sqlite'))
        db.execute('CREATE TABLE IF NOT EXISTS video (bv_id string PRIMARY KEY)')
        db.execute('CREATE TABLE IF NOT EXISTS audio (audio_id string PRIMARY KEY)')
        db.execute('CREATE TABLE IF NOT EXISTS album (doc_id string PRIMARY KEY)')
        db.commit()
        return db

    @staticmethod
    def init_config(cfg_path):
        cfg_path = Path(cfg_path) if cfg_path else os.path.join(Path.cwd(), '.bili_dler')
        os.makedirs(cfg_path, exist_ok=True)
        cfg = ConfigParser()
        cfg.read(os.path.join(cfg_path, 'config.ini'))
        return cfg, cfg_path

    def __del__(self):
        self.tmpdir.cleanup()
        self.db.close()

    def download(self, url):
        if self.dry_run:
            return 0
        fp = os.path.join(self.tmpdir.name, urlparse(url).path.split('/')[-1])
        with (requests.get(url, headers=self.HEADER, cookies=self.cookie, stream=True) as r,
              tqdm.wrapattr(r.raw, "read", total=int(r.headers.get("Content-Length")), desc="") as raw,
              open(fp, mode='wb') as f):
            shutil.copyfileobj(raw, f)
        return fp

    def _download(self, url):
        if self.dry_run:
            return 0
        fp = os.path.join(self.tmpdir.name, urlparse(url).path.split('/')[-1])
        with open(fp, mode='wb') as f:
            f.write(requests.get(url).content)
        return fp

    def examine_history(self, items):
        selected = {'video': [], 'audio': [], 'album': []}
        for item in items['video']:
            bv_id = list(item.values())[0]
            if len(self.db.execute('SELECT * FROM video WHERE bv_id=?', (bv_id, )).fetchall()) == 0:
                selected['video'].append(item)
                self.db.execute('INSERT INTO video VALUES (?)', (bv_id, ))
                self.db.commit()
        for item in items['audio']:
            if len(self.db.execute('SELECT * FROM audio WHERE audio_id=?', (item['id'], )).fetchall()) == 0:
                selected['audio'].append(item)
                self.db.execute('INSERT INTO audio VALUES (?)', (item['id'],))
                self.db.commit()
        for item in items['album']:
            if len(self.db.execute('SELECT * FROM album WHERE doc_id=?', (item['doc_id'], )).fetchall()) == 0:
                selected['album'].append(item)
                self.db.execute('INSERT INTO audio VALUES (?)', (item['doc_id'],))
                self.db.commit()
        return selected
