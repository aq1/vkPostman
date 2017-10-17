from django.core.management.base import BaseCommand

from chat.telegram.commands import AVAILABLE_COMMANDS


class Command(BaseCommand):
    help = 'List available telegram commands in format that can be used with Botfather'

    def handle(self, *args, **options):
        print('\n'.join([
            str(command) for command in AVAILABLE_COMMANDS.values()
        ]))
