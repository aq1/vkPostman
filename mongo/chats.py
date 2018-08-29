from mongo.client import db


def create_chat(vk_id, telegram_id):
    db.chats.update({
        'vk_id': vk_id,
        'telegram_id': telegram_id
    }, {'$set': {
        'vk_active': True,
        'telegram_active': True,
    }}, upsert=True,
    )


def get_chat(vk_id, telegram_id):
    return db.chats.find_one({
        'vk_id': vk_id,
        'telegram_id': telegram_id,
    })


def get_active_chat_by_vk_id(vk_id):
    return db.chats.find_one({
        'vk_id': vk_id,
        'vk_active': True,
        'telegram_active': True,
    })


def get_active_chat_by_telegram_id(telegram_id):
    return db.chats.find_one({
        'telegram_id': telegram_id,
        'vk_active': True,
        'telegram_active': True,
    })


def disable_chat(chat_id):
    db.chats.update(
        {'_id': chat_id},
        {'$set': {'vk_active': False, 'telegram_active': False}},
    )


def get_chats_history(telegram_id):
    return db.chats.find(
        {'telegram_id': telegram_id},
    )
