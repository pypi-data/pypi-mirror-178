import logging

from tqdm.auto import tqdm

from .._base_dler import BaseDler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AlbumDler(BaseDler):
    def __init__(self, sessdata: str, dl_path=None, cfg_path=None, dry_run=False):
        super().__init__(sessdata, dl_path, cfg_path, mode='albums', dry_run=dry_run)

    def __call__(self, *args, **kwargs):
        items = self.parser(*args, **kwargs)
        return self.download_albums(items['albums'])

    def download_albums(self, albums):
        files = {}
        for album in albums:
            logging.info('Downloading Albums: %s', album['doc_id'])
            files[album['doc_id']] = [self.download(picture['img_src']) for picture in tqdm(album['pictures'])]
        return files
