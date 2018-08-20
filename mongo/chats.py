from pymongo.errors import DuplicateKeyError

from mongo.client import db


def get_chat(vk_id, telegram_id):
    return db.chats.find_one({
        'vk_id': vk_id,
        'telegram_id': telegram_id,
    })
#
#
# def save_telegram_user(vk_id, telegram_id):
#     try:
#         db.chats.save({
#             'vk_id': vk_id,
#             'telegram_id': telegram_id,
#         })
#     except DuplicateKeyError:
#         pass
