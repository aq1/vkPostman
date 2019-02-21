import argparse

import sentry_sdk

import settings
import bot
import vk


COMMANDS = {
    'start_bot': bot.start_bot,
    'start_vk_polling': vk.service.start,
}

if not settings.DEBUG:
    sentry_sdk.init(settings.SENTRY_URL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=COMMANDS.keys())

    COMMANDS[parser.parse_args().command]()


if __name__ == '__main__':
    main()
