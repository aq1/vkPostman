from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.commands import BaseCommand, ConnectCommand, DisconnectCommand
import mongo


class Chats(BaseCommand):
    _COMMAND = 'chats'
    _DESCRIPTION = 'Show my chats.'
    _SUCCESS_MSG = ''

    def _call(self, user, _bot, update, **kwargs):
        chats = list(mongo.chats.get_chats_history(user.id))
        if not chats:
            update.message.reply_text(
                text='No chats history. Connect to a user and his name will be shown here.'
            )
            return

        vk_users = {
            vk_user['id']: vk_user
            for vk_user in mongo.users.get_vk_users_by_id([c['vk_id'] for c in chats])
        }

        reply_markup = []
        for chat in chats:
            text = '{} {}'.format(
                vk_users[chat['vk_id']]['first_name'],
                vk_users[chat['vk_id']]['last_name'],
            )
            if chat['vk_active'] and chat['telegram_active']:
                text = '✅ {}'.format(text)

            connect_callback = '{} {}'.format(ConnectCommand.get_command(), chat['vk_id'])
            disconnect_callback = '{}'.format(DisconnectCommand.get_command())

            reply_markup.append([
                InlineKeyboardButton(text, callback_data=connect_callback),
                InlineKeyboardButton('🗑', callback_data=disconnect_callback),
            ])

        update.message.reply_text(
            text=(
                'Your chats.\n'
                'Click name to connect or disconnect.\n'
                '✅ means you are connected\n'
                '🗑 to remove chat from history.'
            ),
            reply_markup=InlineKeyboardMarkup(reply_markup),
            disable_web_page_preview=True,
        )
