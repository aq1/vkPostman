from chat.telegram.commands.command_base import CommandBase
from chat.telegram.commands.connect import Connect
from chat.telegram.commands.disconnect import Disconnect
from chat.telegram.commands.start import Start
from chat.telegram.commands.help import Help
from chat.telegram.commands.chats import Chats
from chat.telegram.commands.message_to_admin import MessageToAdmin
from chat.telegram.commands.remove_chat import RemoveChat

from chat.telegram.commands.execute_command import (
    execute_command,
    parse_and_execute_telegram_command,
    execute_command_from_callback_query,
    AVAILABLE_COMMANDS,
)
