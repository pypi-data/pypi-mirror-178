from src.bili_downloader import BiliDownloader, VideoDler, UpDler


if __name__ == '__main__':
    # d = VideoDler(sessdata='b4f0af61%2C1659237450%2C8f896*21', dl_path='/Volumes/THL/影片', dry_run=True)
    # x = d('https://www.bilibili.com/video/BV1J4411v7g6')
    d = UpDler(sessdata='b4f0af61%2C1659237450%2C8f896*21', dl_path='/Volumes/THL/影片', dry_run=True)
    # d = BiliDownloader(sessdata='b4f0af61%2C1659237450%2C8f896*21', dl_path='/Volumes/THL/影片')
    d(353837540)
    # d(['https://www.bilibili.com/video/BV1J4411v7g6']) # 353837540

    i = 0
