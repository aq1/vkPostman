import bot
import vk

import multiprocessing


if __name__ == '__main__':
    for f in bot.start_bot, vk.service.start:
        p = multiprocessing.Process(target=f)
        p.start()
