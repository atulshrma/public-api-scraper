import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from pymongo import MongoClient


async_mongo_client: AsyncIOMotorClient = None
sync_mongo_client: MongoClient = None


def get_async_mongo_conn():
    global async_mongo_client

    if not async_mongo_client:
        async_mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URI"])

    return async_mongo_client[os.environ["DB_NAME"]]


def close_async_mongo_conn():
    global async_mongo_client

    if not async_mongo_client:
        return

    async_mongo_client.close


def get_sync_mongo_conn():
    global sync_mongo_client

    if not sync_mongo_client:
        sync_mongo_client = MongoClient(os.environ["MONGODB_URI"])

    return sync_mongo_client[os.environ["DB_NAME"]]


def close_sync_mongo_conn():
    global sync_mongo_client

    if not sync_mongo_client:
        return

    sync_mongo_client.close()
