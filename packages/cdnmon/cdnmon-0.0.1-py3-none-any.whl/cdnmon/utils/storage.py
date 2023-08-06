import os
import time

from pymongo import MongoClient

from cdnmon.utils.logging import logger
from minio import Minio


def connect_minio():
    try:
        client = Minio(
            os.environ["MINIO_HOST"],
            access_key=os.environ["MINIO_ACCESS_KEY"],
            secret_key=os.environ["MINIO_SECRET_KEY"],
        )
        logger.success(f"MinIO endpoint {os.environ['MINIO_HOST']} connected")
        return client
    except Exception as e:
        logger.error(e)
        return None


def connect_mongodb():
    try:
        client = MongoClient(os.environ["MONGODB_URI"], tls=True)
        logger.success("MongoDB endpoint connected")
        return client
    except Exception as e:
        logger.error(e)
        return None


mongodb_client = connect_mongodb()
minio_client = connect_minio()


def save_to_minio(filepath, object_name):
    if not minio_client:
        return
    try:
        bucket_name = os.environ["MINIO_BUCKET_NAME"]
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
        minio_client.fput_object(bucket_name, object_name, filepath)
        logger.success(f"{filepath} saved into {object_name} ({bucket_name})")
    except Exception as e:
        logger.error(e)


def mongodb_save(cdn_name, ipv4_networks, ipv6_networks):
    if not mongodb_client:
        return
    try:
        db = mongodb_client[cdn_name]["ip_ranges"]
        created = db.insert_one(
            {
                "timestamp": time.time(),
                "ipv4_prefixes": [str(network) for network in ipv4_networks],
                "ipv6_prefixes": [str(network) for network in ipv6_networks],
            }
        )
        logger.success(f"{created} saved")
    except Exception as e:
        logger.error(e)
