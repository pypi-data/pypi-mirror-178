import os
import cv2 as cv
from mutagen.mp4 import MP4, MP4Cover

from ._converter import merge


def apple_music(audio, music_path, metadata=None, cover=None, lyric=None):
    music_path = merge(output=os.path.join(music_path, metadata['\xa9nam'] + '.m4a'), audio=audio)

    with MP4(music_path) as fm:
        fm.update(metadata)
        if lyric:
            with open(lyric) as f:
                audio['\xa9lyr'] = f.read()
        if cover:
            img = cv.imread(cover)
            h, w, _ = img.shape
            if h % 2 == 1:
                h -= 1
            if w % 2 == 1:
                w -= 1
            cv.imwrite(cover, img[:h, :w])
            with open(cover, "rb") as f:
                fm["covr"] = [MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_PNG)]
    fm.save()
