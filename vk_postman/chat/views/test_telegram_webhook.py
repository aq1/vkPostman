from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

import requests


@csrf_exempt
def test_telegram_webhook(request):
    url = '{}{}'.format(settings.TEST_HOST, reverse('telegram_webhook'))
    print(url)
    try:
        r = requests.post(
            url,
            data=request.body
        )
    except requests.RequestException as e:
        print(e)
    else:
        print(r)
    return HttpResponse(status=200)
