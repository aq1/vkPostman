import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from chat.vk.vk_chat import send_message_from_telegram_to_vk
from chat.telegram.commands import (
    parse_and_execute_telegram_command,
    execute_command_from_callback_query,
)


@csrf_exempt
def telegram_webhook(request):
    try:
        data = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    print(request.body)

    if data.get('message'):
        for entity in data['message'].get('entities', []):
            if entity.get('type') == 'bot_command':
                parse_and_execute_telegram_command(entity, data)
                return HttpResponse()
        send_message_from_telegram_to_vk(data)

    elif data.get('callback_query'):
        execute_command_from_callback_query(data)
        return HttpResponse()
    else:
        return HttpResponse(status=202, content=b'Unknown message type')

    return HttpResponse()
