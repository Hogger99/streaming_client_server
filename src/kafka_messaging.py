import argparse
import sys
import os
import yaml
from kafka3 import KafkaProducer, KafkaConsumer
from kafka3.errors import KafkaTimeoutError
from kafka3.errors import KafkaError
import json


def produce_connection(cfg):

    if 'KAFKA' in cfg:
        producer = KafkaProducer(bootstrap_servers=[cfg['KAFKA']['BOOTSTRAP_SERVERS']],
                                 api_version=tuple(cfg['KAFKA']['VERSION']),
                                 acks='all',
                                 client_id=cfg['KAFKA']['PRODUCER_CLIENT_ID'],
                                 value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                                 compression_type=cfg['KAFKA']['COMPRESSION']
                                 )

    else:
        print(f"error missing KAFKA in cfg")
        producer = None

    return producer


def consume_connection(cfg):
    if 'KAFKA' in cfg:
        consumer = KafkaConsumer(bootstrap_servers=[cfg['KAFKA']['BOOTSTRAP_SERVERS']],
                                 api_version=tuple(cfg['KAFKA']['VERSION']),
                                 group_id=None,
                                 client_id=cfg['KAFKA']['CONSUMER_CLIENT_ID'],
                                 value_deserializer=lambda m: json.loads(m.decode()),
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False
                                 )
        # subscribe to the topic
        consumer.subscribe(cfg['KAFKA']['TOPIC'])
    else:
        print(f"error missing KAFKA in cfg")
        consumer = None
    return consumer



