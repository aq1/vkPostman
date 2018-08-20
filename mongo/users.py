from pymongo.errors import DuplicateKeyError

from mongo.client import db


def get_telegram_user(chat_id):
    return db.telgeram_users.find_one({
        'id': chat_id,
    })


def save_telegram_user(user):
    try:
        db.telgeram_users.save({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    except DuplicateKeyError:
        pass


def get_vk_user(vk_id):
    return db.vk_users.find_one({
        'id': vk_id,
    })


def save_vk_user(user):
    try:
        db.vk_users.save({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    except DuplicateKeyError:
        pass
