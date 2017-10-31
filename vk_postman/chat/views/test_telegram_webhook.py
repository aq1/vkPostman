from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_telegram_webhook(request):
    return redirect('{}/{}'.format(settings.TEST_HOST, settings.TELEGRAM_WEBHOOK_PATH))
