# -*- coding: utf-8 -*-

import sys
import time

from argparse import ArgumentParser
from ConfigParser import ConfigParser
from logging import basicConfig, getLogger, INFO
from mastodon import Mastodon
from retry import retry
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

parser = ArgumentParser(
    prog="TOMOYODon"
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-t', '--token',
    action='store_true',
    help='get access token'
)


basicConfig(level=INFO)
logger = getLogger(__name__)


def get_access_token():
    config = ConfigParser()
    config.readfp(open('token.ini'))

    section = 'Token'
    api_base_url = config.get(section, 'api_base_url')
    username = config.get(section, 'username')
    password = config.get(section, 'password')

    client_id = config.get(section, 'client_id')
    access_token = config.get(section, 'access_token')
    scopes = ['read', 'write']

    Mastodon.create_app(
        'TOMOYODon',
        scopes=scopes,
        api_base_url=api_base_url,
        to_file=client_id
    )

    mastodon = Mastodon(
        client_id=client_id,
        api_base_url=api_base_url
    )

    mastodon.log_in(
        username=username,
        password=password,
        scopes=scopes,
        to_file=access_token
    )


class ChangeHandler(FileSystemEventHandler):

    def __init__(self, mastodon, toot_str, sensitive, visibility):
        self.mastodon = mastodon
        self.toot_str = toot_str
        self.sensitive = sensitive
        self.visibility = visibility

    def on_created(self, event):
        if event.is_directory:
            return

        logger.info(event.src_path)
        media_ids = []
        media = self.media_post(event.src_path)
        media_ids.append(media)
        self.mastodon.status_post(
            self.toot_str,
            media_ids=media_ids,
            sensitive=self.sensitive,
            visibility=self.visibility
        )

    @retry(IOError, delay=1)
    def media_post(self, path):
        return self.mastodon.media_post(path)


def toot():
    config = ConfigParser()
    config.readfp(open('tomoyodon.ini'))
    section_api = 'API'

    mastodon = Mastodon(
        client_id=config.get(section_api, 'client_id'),
        access_token=config.get(section_api, 'access_token'),
        api_base_url=config.get(section_api, 'api_base_url')
    )

    target_path = config.get('Path', 'target')

    section_toot = 'TOOT'
    toot_str = config.get(section_toot, 'toot_str')
    sensitive = config.getboolean(section_toot, 'sensitive')
    visibility = config.get(section_toot, 'visibility')

    event_handler = ChangeHandler(mastodon, toot_str, sensitive, visibility)
    observer = Observer()
    observer.schedule(event_handler, target_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    args = parser.parse_args(sys.argv[1:])

    if args.token:
        get_access_token()
        sys.exit(0)
    else:
        toot()

if __name__ == '__main__':
    main()
