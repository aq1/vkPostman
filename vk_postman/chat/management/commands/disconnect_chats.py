from django.core.management.base import BaseCommand

from chat.models import Chat


class Command(BaseCommand):
    help = 'Disconnect chats. Provide vk user ids or type \'all\' to disconnect all chats'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', default=False)
        parser.add_argument('--vk_ids', action='store')

    def handle(self, *args, **options):
        if options['all'] == options['vk_ids']:
            self.stdout.write(self.style.ERROR('Only one argument should be provided: --all or --vk_ids'))
            return
        print(Chat.disconnect(options['vk_ids']))
