import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from chat.telegram.commands import execute_command
from chat.vk.vk_chat import send_message_from_telegram_to_vk


@csrf_exempt
def telegram_webhook(request):
    try:
        data = json.loads(request.body.decode())
        from_ = data['message']['from']
    except (KeyError, json.JSONDecodeError):
        return HttpResponse(status=400)
    print(data)
    text = data['message'].get('text', '')
    for entiy in data['message'].get('entities', []):
        if entiy.get('type') == 'bot_command':
            offset, length = entiy.get('offset', 0), entiy.get('length', 0)
            command, args = text[offset:offset + length], text.split(' ')[1:]
            execute_command(from_, command, args)
            return HttpResponse()

    send_message_from_telegram_to_vk(from_['id'], text)
    return HttpResponse()
