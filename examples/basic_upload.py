"""Gets a video from the internet and uploads it"""

from random import choice
from matplotlib.pylab import choice

from tiktok_uploader.upload import TikTokUploader


if __name__ == "__main__":
    BROWSERS = [
    'chrome',
]

# single video
uploader = TikTokUploader(cookies='www.tiktok.com_cookies.txt', browser=choice(BROWSERS), headless=False)
uploader.upload_video('newVideo123.mp4', description='#fyp #foryou #rec #viral #trending #funny #comedy #memes #tiktok #minecraft')

