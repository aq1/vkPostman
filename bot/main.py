import telegram
import telegram.ext
import telegram.utils.request

from utils.logging import bot_logger
import settings
import bot

commands = [
    bot.commands.StartCommand(),
    bot.commands.HelpCommand(),
    bot.commands.ConnectCommand(pass_args=True),
    bot.commands.DisconnectCommand(),
    bot.commands.MessageToAdminCommand(pass_args=True),
    bot.commands.Chats(),
    bot.commands.History(pass_args=True),
    bot.commands.RemoveChat(pass_args=True),
]

callback_queries = [
    telegram.ext.CallbackQueryHandler(
        bot.commands.ConnectCommand(),
        pattern='{} \d+'.format(bot.commands.ConnectCommand.get_command()),
    ),
    telegram.ext.CallbackQueryHandler(
        bot.commands.DisconnectCommand(),
        pattern='{} \d+'.format(bot.commands.DisconnectCommand.get_command()),
    ),
]

messages_transport = [
    bot.message_transport.TransportMessageToVK()
]

states = commands + callback_queries + messages_transport

bot_handler = telegram.ext.ConversationHandler(
    entry_points=states,
    states={
        bot.states.START: states,
    },
    fallbacks=[telegram.ext.RegexHandler('.+', lambda *args: bot.states.START)],
)


def start_bot():
    _request = telegram.utils.request.Request(con_pool_size=8)
    _bot = telegram.Bot(token=settings.TELEGRAM_TOKEN, request=_request)
    updater = telegram.ext.Updater(bot=_bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(bot_handler)

    bot_logger.info('Printing available commands')
    bot_logger.info('\n'.join(map(str, commands)))
    bot_logger.info('Started Bot')

    _bot.sendMessage(settings.ADMIN_ID, 'Started bot')

    updater.start_polling(clean=True)
