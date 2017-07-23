import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from chat.telegram.commands import execute_command
from chat.vk.vk_chat import send_message_from_telegram_to_vk


@csrf_exempt
def telegram_webhook(request):
    try:
        data = json.loads(request.body.decode())
        telegram_user_id = data['message']['from']['id']
    except (KeyError, json.JSONDecodeError):
        return HttpResponse(status=400)

    text = data['message']['text']
    for entiy in data['message'].get('entities', []):
        if entiy.get('type') == 'bot_command':
            offset, length = entiy.get('offset', 0), entiy.get('length', 0)
            command, args = text[offset:offset + length], text.split(' ')[1:]
            execute_command(command, telegram_user_id, args)
            return HttpResponse()

    send_message_from_telegram_to_vk(telegram_user_id, text)
    return HttpResponse()
