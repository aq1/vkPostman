from collections import OrderedDict

from chat.telegram import commands


AVAILABLE_COMMANDS = OrderedDict()
for attr in dir(commands):
    instance = getattr(commands, attr)
    try:
        if issubclass(instance, commands.CommandBase) and instance is not commands.CommandBase:
            AVAILABLE_COMMANDS[instance.__name__.lower()] = instance
    except TypeError:
        pass


def execute_command(from_, command, args=None):
    command = command.lstrip('/')
    if command not in AVAILABLE_COMMANDS:
        commands.CommandBase.send_message(from_['id'], 'Sorry! No command with the name {} found'.format(command))
        return

    if args is None:
        args = []

    AVAILABLE_COMMANDS[command].execute(from_, args)


def parse_and_execute_telegram_command(entity, data):
    offset, length = entity.get('offset', 0), entity.get('length', 0)
    text = data['message'].get('text', '')
    command, args = text[offset:offset + length], text.split()[1:]
    execute_command(data['message']['from'], command, args)


def execute_command_from_callback_query(data):
    from_ = data['callback_query']['message']['chat']
    text = data['callback_query']['data']
    command, *args = text.lstrip('/').split()
    execute_command(from_, command, args)
