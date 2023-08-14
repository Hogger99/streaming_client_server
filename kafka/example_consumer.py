import argparse
import sys
import os
import yaml
from kafka3 import KafkaConsumer
from kafka3.errors import KafkaTimeoutError
from kafka3.errors import KafkaError
import json


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", "-c", required=True, action='store', help='the config file for this program')

    parsed, unknown = parser.parse_known_args(sys.argv[1:])

    args = vars(parsed)

    if 'cfg' in args and args['cfg'] is not None and len(args['cfg']) > 0:
        config_file_name = args['cfg']

        if os.path.exists(config_file_name):
            try:
                with open(config_file_name, 'rt') as cfg_handle:
                    cfg = yaml.full_load(cfg_handle)

                if 'KAFKA' in cfg:
                    consumer = KafkaConsumer(bootstrap_servers=[cfg['KAFKA']['BOOTSTRAP_SERVERS']],
                                             api_version=tuple(cfg['KAFKA']['VERSION']),
                                             group_id=None,
                                             client_id=cfg['KAFKA']['CONSUMER_CLIENT_ID'],
                                             value_deserializer=lambda m: json.loads(m.decode()),
                                             auto_offset_reset='earliest',
                                             enable_auto_commit=False
                                             )
                    consumer.subscribe(cfg['KAFKA']['TOPIC'])

                    print('connected now listening')
                    for message in consumer:
                        print(f"{message.topic}:{message.partition}:{message.offset}")
                        print(f"{message.value}")

                else:
                    print(f"error missing KAFKA in file {config_file_name}")

            except Exception as e:
                print(f"error {e}")

        else:
            print(f"error missing config file {config_file_name}")

    else:
        print("error missing config file")
