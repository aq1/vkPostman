import vk
import mongo
import settings
from bot.commands import BaseCommand


class History(BaseCommand):
    _COMMAND = 'history'
    _DESCRIPTION = 'Show recent VK history with current user'

    @staticmethod
    def _format_message(msg):
        if msg['from_id'] == settings.VK_ADMIN_ID:
            msg = msg['body'].splitlines()
            msg[0] = '▫<b>{}</b>'.format(msg[0])
            return '\n'.join(msg)
        else:
            user = vk.functions.get_vk_user(msg['from_id'])
            return '▪<b>{} {}</b>\n{}'.format(
                user['first_name'],
                user['last_name'],
                msg['body'],
            )

    def _call(self, user, _bot, update, **kwargs):
        try:
            vk_id = int(kwargs['args'][0])
        except ValueError:
            update.message.reply_text(
                text='VK id must be an integer',
            )
            return
        except IndexError:
            chat = mongo.chats.get_active_chat_by_telegram_id(user['id'])
        else:
            chat = mongo.chats.get_chat(vk_id, user['id'])
            if not chat:
                update.message.reply_text(
                    text='You have not got history with this user',
                )
                return

        if not chat:
            update.message.reply_text(
                text=(
                    'You need to be connected '
                    'to a user to get chat history or provide a VK id'
                )
            )
            return

        history = vk.functions.get_history(chat['vk_id'])

        text = '\n'.join([
            self._format_message(msg)
            for msg in reversed(history['response']['items'])
            if msg['body']
        ])

        update.message.reply_text(
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True,
        )
