# -*- coding:utf-8 -*-


VERSION = '1.0.9'

AUTHOR = "cn"

AUTHOR_EMAIL = "308299269@qq.com"

URL = "https://www.github.com/ShichaoMa/webWalker"

from redis_feed import RedisFeed

def main():
    RedisFeed.parse_args().start()