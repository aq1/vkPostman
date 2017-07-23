from chat.telegram import commands


AVAILABLE_COMMANDS = {}
for attr in dir(commands):
    instance = getattr(commands, attr)
    try:
        if issubclass(instance, commands.CommandBase) and instance is not commands.CommandBase:
            AVAILABLE_COMMANDS[instance.__name__.lower()] = instance
    except TypeError:
        pass


def execute_command(command, telegram_user_id, args=None):
    command = command.replace('/', '')
    if command not in AVAILABLE_COMMANDS:
        commands.CommandBase.send_message(telegram_user_id, 'Sorry! No command with the name {} found'.format(command))
        return

    if args is None:
        args = []

    AVAILABLE_COMMANDS[command].execute(telegram_user_id, *args)
