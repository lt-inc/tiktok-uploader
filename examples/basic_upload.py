"""Gets a video from the internet and uploads it"""

from random import choice

from tiktok_uploader.upload import TikTokUploader


if __name__ == "__main__":
    BROWSERS = [
    'chrome',
]

# single video
uploader = TikTokUploader(cookies='www.tiktok.com_cookies.txt', browser="chrome", headless=True)
uploader.upload_video('0.mp4', description='#fyp')

