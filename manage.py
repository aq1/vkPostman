import os
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
    arguments = parser.parse_args()

    pid_path = os.path.join(settings.PID_DIR_PATH, 'vk_postman_{}.pid'.format(arguments.command))
    with open(pid_path, 'w') as f:
        f.write(str(os.getpid()))

    COMMANDS[arguments.command]()


if __name__ == '__main__':
    main()
