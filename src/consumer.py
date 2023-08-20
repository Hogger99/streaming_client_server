from kafka3 import KafkaConsumer
import argparse
import sys
import os
from src.file_reader import read_yaml_file
import json
from src.stack_db import configure_db,  insert_test_data


def consume_messages(config_file):

    # check that we have all the right config keys in the config file
    #
    if os.path.exists(config_file):
        cfg = read_yaml_file(config_file)

        # setup db
        db_str = f"host={cfg['DATABASE']['HOST']} port={cfg['DATABASE']['PORT']} dbname={cfg['DATABASE']['DBNAME']} user={cfg['DATABASE']['DBUSER']} password={cfg['DATABASE']['USER_PWD']}"

        error = configure_db(db=db_str)

        # connect to kafka
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

        #

        # if we connected to kafka then consume from kafka in infinite loop
            print('connected now listening')
            for message in consumer:
                uid = f"{message.offset}_{message.timestamp}"
                print(f"{uid} {message.value}")

                if 'name' in message.value and 'age' in message.value:
                    insert_test_data(db=db_str,
                                     name=message.value['name'],
                                     age=message.value['age'],
                                     uid=uid,
                                     msg=message.value)
                else:
                    insert_test_data(db=db_str,
                                     uid=uid,
                                     msg=message.value)

        else:
            print(f"error missing KAFKA in file {config_file}")
    # for each look get data from message and call insert routine

    else:
        print("error missing config file")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", "-c", required=True, action='store', help='the config file for this program')

    parsed, unknown = parser.parse_known_args(sys.argv[1:])

    args = vars(parsed)

    consume_messages(config_file=args['cfg'])
    