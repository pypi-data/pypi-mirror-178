import os
import logging
import tempfile

from .converter import apple_music, merge
from ._base_dler import BaseDler
from .downloader import Video, Audio, Album, Dynamic, Manga

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BiliDownloader(BaseDler):
    def __init__(self, sessdata: str, mode, dl_path=None, cfg_path=None, dry_run=False):
        """

        :param sessdata: Bilibili Login Cookie
        :param dl_path:
        :param cfg_path:
        """
        super().__init__(sessdata, dl_path, cfg_path)
        self.mode = self.parse_mode(mode)

    def __call__(self, *args, **kwargs):
        items = self.parser(*args, **kwargs)

        # with open('parse.json') as f:
        #     import json
        #     items = json.load(f)
        items = self.examine_history(items)

        with tempfile.TemporaryDirectory() as tmpdir:
            if 'video' in self.mode:
                videos = download_videos(items['video'], tmpdir, self.cookie, video=video, audio=audio)
                for k, v in videos.items():
                    merge(v['video'], v['audio'], os.path.join(self.dl_path, v['metadata']['\xa9nam'] + '.mov'))
            if audio:
                audios = download_audios(items['audio'], tmpdir, self.cookie)
            if album:
                albums = download_albums(items['album'], tmpdir)

            if music:
                for k, v in videos.items():
                    if k != 'cover':
                        fp = os.path.join(self.dl_path, v['metadata']['\xa9nam'] + '.m4a')
                        apple_music(v['audio'], fp, metadata=v['metadata'], cover=videos['cover'])
                for k, a in audios.items():
                    fp = os.path.join(self.dl_path, a['metadata']['\xa9nam'] + '.m4a')
                    apple_music(a['audio'], fp, metadata=a['metadata'], cover=a['cover'], lyric=a['lyric'])

    @staticmethod
    def parse_mode(mode: [list, tuple, str]):
        if isinstance(mode, str):
            mode = mode.split(',')
        if isinstance(mode, (list, tuple)):
            mode = set(mode)
            if 'up' in mode:
                mode.add(['video', 'audio', 'album'])
            if 'music' in mode:
                mode.add(['audio', 'video'])
            return mode
        else:
            raise TypeError('mode must be list, tuple or str')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('sessdata', help='Bilibili Login Cookie')
    parser.add_argument('mode', help='Download Mode')
    parser.add_argument('dl_path', help='Download Path')
    parser.add_argument('cfg_path', help='Config Path')
    args = parser.parse_args()
    b = BiliDownloader(args.sessdata, args.mode, args.dl_path, args.cfg_path)
    b()

if __name__ == '__main__':
    main()
