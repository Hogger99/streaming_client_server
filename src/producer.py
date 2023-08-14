from file_reader import read_yaml_file, read_json_file
from kafka_messaging import produce_connection
import argparse
import sys
import os
import yaml
import json
from kafka3.errors import KafkaTimeoutError
from kafka3.errors import KafkaError
from time import sleep



def run(config_file, directory):
    if os.path.exists(config_file) and os.path.exists(directory):
        cfg = read_yaml_file(config_file)
        producer = produce_connection(cfg=cfg)
        files_sent = []
        error = False
        while not error:
            sleep(5)
            file_list = os.listdir(directory)
            for file in file_list:
                if (os.path.isfile(os.path.join(directory, file)) and
                        (".json" in file or ".yml" in file) and
                        file not in files_sent):
                    if ".json" in file:
                        contents = read_json_file(os.path.join(directory, file))
                    elif ".yml" in file:
                        contents = read_yaml_file(os.path.join(directory, file))
                    else:
                        contents = None



                    if contents is not None:
                        try:
                            future = producer.send(cfg['KAFKA']['TOPIC'], contents)
                            meta_data = future.get(timeout=30)
                            files_sent.append(file)
                            print(f'{file} sent successfully')




                        except (KafkaTimeoutError, KafkaError) as e:
                            error = True
                            print(f"{e}")


    else:
        print(f'{config_file} does not exist')



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", "-c", required=True, action='store', help='the config file for this program')
    parser.add_argument("--dir", "-d", required=True, action='store', help='directory to monitor for data to send to Kafka')

    parsed, unknown = parser.parse_known_args(sys.argv[1:])

    args = vars(parsed)
    run(config_file=args["cfg"], directory=args["dir"])
