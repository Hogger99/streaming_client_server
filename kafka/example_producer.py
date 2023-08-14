import argparse
import sys
import os
import yaml
from kafka3 import KafkaProducer
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
                    producer = KafkaProducer(bootstrap_servers=[cfg['KAFKA']['BOOTSTRAP_SERVERS']],
                                             api_version=tuple(cfg['KAFKA']['VERSION']),
                                             acks='all',
                                             client_id=cfg['KAFKA']['PRODUCER_CLIENT_ID'],
                                             value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                                             compression_type=cfg['KAFKA']['COMPRESSION']
                                             )

                    try:
                        for idx in range(10):
                            test_msg = {'NAME': 'stephen',
                                        'ID': idx}

                            future = producer.send(cfg['KAFKA']['TOPIC'],
                                                   test_msg)
                            meta_data = future.get(timeout=30)
                    except (KafkaTimeoutError, KafkaError) as e:
                        print(f"{e}")
                else:
                    print(f"error missing KAFKA in file {config_file_name}")

            except Exception as e:
                print(f"error {e}")

        else:
            print(f"error missing config file {config_file_name}")

    else:
        print("error missing config file")
