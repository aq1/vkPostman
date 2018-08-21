from pymongo.errors import DuplicateKeyError

from mongo.client import db


def get_telegram_user(chat_id):
    return db.telegram_users.find_one({
        'id': chat_id,
    })


def save_telegram_user(user):
    try:
        db.telegram_users.save({
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
    user = {
        'id': user['id'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
    }
    db.vk_users.update(user, user, upsert=True)
    return user
