import os
import logging

from .._base_dler import BaseDler
from ..converter import merge as _merge, apple_music
from .video import VideoDler
from .audio import AudioDler
from .albums import AlbumDler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UpDler(BaseDler):
    def __init__(self, sessdata, dl_path=None, cfg_path=None,
                 merge=True, album=True, video=True, audio=True, music=True, dry_run=False):
        self.video = VideoDler(sessdata, dl_path, cfg_path, dry_run=dry_run) if video else None
        self.merge = merge
        self.audio = AudioDler(sessdata, dl_path, cfg_path, dry_run=dry_run) if audio else None
        self.album = AlbumDler(sessdata, dl_path, cfg_path, dry_run=dry_run) if album else None
        self.apple_music = music

        super().__init__(sessdata=sessdata, dl_path=dl_path, cfg_path=cfg_path, mode='up', dry_run=dry_run)

    def __call__(self, *args, **kwargs):
        items = self.parser(*args, **kwargs)
        files = {}
        if self.video:
            videos = self.video.download_videos(items['video'], video=bool(self.video), audio=bool(self.audio))
            files['video'] = [_merge(os.path.join(self.dl_path, f'{video}_{page}.mov'), video=info['video'],
                                     audio=info['audio']) for video, pages in videos.items()
                              for page, info in pages.items()] if self.merge and not self.dry_run else videos
        if self.audio:
            audios = self.audio.download_audios(items['audio'])
            files['audio'] = [apple_music(audio=audio['audio'], music_path=self.dl_path, metadata=audio['metadata'],
                                          lyric=audio['lyric'], cover=audio['cover'])
                              for aid, audio in audios.items()] if self.apple_music and not self.dry_run else audios
        if self.album:
            files['albums'] = self.album.download_albums(items['album'])

        return files
