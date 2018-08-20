import telegram
import telegram.ext

from utils.logging import logger
import settings
import bot

commands = [
    bot.commands.StartCommand(),
    bot.commands.HelpCommand(),
    bot.commands.ConnectCommand(pass_args=True),
]

bot_handler = telegram.ext.ConversationHandler(
    entry_points=commands,
    states={
        bot.states.START: commands,
    },
    fallbacks=[telegram.ext.RegexHandler('\w+', lambda *args: bot.states.START)]
)


def start_bot():
    _bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    updater = telegram.ext.Updater(bot=_bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(bot_handler)
    logger.info('Printing available commands')
    logger.info('\n'.join(map(str, commands)))
    logger.info('Started Bot')
    try:
        updater.start_polling(clean=True)
    except KeyboardInterrupt:
        logger.info('Stopped Bot')
