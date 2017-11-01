import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from chat.telegram.commands import execute_command
from chat.vk.vk_chat import send_message_from_telegram_to_vk


@csrf_exempt
def telegram_webhook(request):
    try:
        data = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    print(request.body)

    if data.get('message'):
        from_ = data['message']['from']
        text = data['message'].get('text', '')
        for entity in data['message'].get('entities', []):
            if entity.get('type') == 'bot_command':
                offset, length = entity.get('offset', 0), entity.get('length', 0)
                command, args = text[offset:offset + length], text.split()[1:]
                execute_command(from_, command, args)
                return HttpResponse()
        send_message_from_telegram_to_vk(from_['id'], text)

    elif data.get('callback_query'):
        from_ = data['callback_query']['message']['chat']
        text = data['callback_query']['data']
        command, *args = text.lstrip('/').split()
        execute_command(from_, command, args)
        return HttpResponse()
    else:
        return HttpResponse(status=202, content=b'Unknown message type')

    return HttpResponse()
