import os
import argparse

import sentry_sdk
from daemonize import Daemonize

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
    parser.add_argument('-d', '--daemonize', default=False, action='store_true')

    with open(settings.PID_FILE_PATH, 'w') as f:
        f.write(str(os.getpid()))

    arguments = parser.parse_args()
    command = COMMANDS[arguments.command]

    if arguments.daemonize:
        Daemonize(
            app='vk_postman_{}'.format(arguments.command),
            pid=settings.PID_FILE_PATH,
            action=command,
        ).start()
        return

    command()


if __name__ == '__main__':
    main()
