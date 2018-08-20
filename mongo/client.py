from pymongo import MongoClient

import settings

client = MongoClient(
    '{}:{}'.format(settings.MONGO_HOST, settings.MONGO_PORT),
    username=settings.MONGO_USER,
    password=settings.MONGO_PASSWORD,
    authSource=settings.MONGO_DB,
    connect=True,
    serverSelectionTimeoutMS=1000,
    authMechanism='SCRAM-SHA-1',
)

db = client[settings.MONGO_DB]
db.telegram_users.create_index('id', unique=True)
db.vk_users.create_index('id', unique=True)
