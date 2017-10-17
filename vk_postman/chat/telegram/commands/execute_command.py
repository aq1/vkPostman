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
    command = command.replace('/', '')
    if command not in AVAILABLE_COMMANDS:
        commands.CommandBase.send_message(from_['id'], 'Sorry! No command with the name {} found'.format(command))
        return

    if args is None:
        args = []

    AVAILABLE_COMMANDS[command].execute(from_, args)
