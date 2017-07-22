from django.core.management.base import BaseCommand

from chat.vk.vk_polling_service import watch_chat


class Command(BaseCommand):
    help = 'Starts vk polling service that watches tha chat'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting polling service'))
        try:
            watch_chat()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Stopped polling service'))
