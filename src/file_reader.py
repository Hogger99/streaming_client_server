# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import yaml
from os.path import exists
import json
import argparse


def read_yaml_file(file_name):
    if exists(file_name):
        with open(file_name, 'rt') as file:
            contents = yaml.safe_load(file)
            return contents
    else:
        contents = f"error {file_name} does not exist"
        print(contents)
        return contents

def read_json_file(file_name):
    if exists(file_name):
        with open(file_name, 'rt') as file:
            contents = file.read()
            contents = json.loads(contents)
            return contents
    else:
        contents = f"error {file_name} does not exist"
        print(contents)
        return contents





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = read_yaml_file("test/test_data.yml")
    print(x)