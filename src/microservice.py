from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn
from pydantic import BaseModel
from src.stack_db import select_test_data
import threading
import argparse
from src.consumer import consume_messages
import sys
from typing import Any, Optional
import os
from src.file_reader import read_yaml_file


class Query(BaseModel):
    key: Optional[str]
    value: Optional[Any]
    name: Optional[str]
    age: Optional[int]


app = FastAPI()

config_file_name: Optional[str] = None


@app.post("/api/v1/query_unstructured_data")
def query_unstructured_data(query: Query):
    global config_file_name

    if query.key is not None and query.value is not None:

        if os.path.exists(config_file_name):
            cfg = read_yaml_file(config_file_name)

            # setup db
            db_str = f"host={cfg['DATABASE']['HOST']} port={cfg['DATABASE']['PORT']} dbname={cfg['DATABASE']['DBNAME']} user={cfg['DATABASE']['DBUSER']} password={cfg['DATABASE']['USER_PWD']}"

            key_to_query = query.key
            value_to_query = query.value

            records, error = select_test_data(db=db_str,
                                              where={f"msg ->> '{key_to_query}' =": value_to_query})
        else:
            error = 'could not read config file'
            records = None

    else:
        error = 'query.key and query.value are None'
        records = None

    if error is None:
        return records
    else:
        raise HTTPException(status_code=404, detail=error)

@app.post("/api/v1/query_relational_data")
def query_relational_data(query: Query):
    global config_file_name

    if query.age is not None or query.name is not None:

        if os.path.exists(config_file_name):
            cfg = read_yaml_file(config_file_name)

            # setup db
            db_str = f"host={cfg['DATABASE']['HOST']} port={cfg['DATABASE']['PORT']} dbname={cfg['DATABASE']['DBNAME']} user={cfg['DATABASE']['DBUSER']} password={cfg['DATABASE']['USER_PWD']}"

            where = {}

            if query.age is not None:
                where['age ='] = query.age

            if query.name is not None:
                where['name ='] = query.name

            records, error = select_test_data(db=db_str,
                                              where=where)
        else:
            error = 'could not read config file'
            records = None

    else:
        error = 'query.age and query.name are None'
        records = None

    if error is None:
        return records
    else:
        raise HTTPException(status_code=404, detail=error)

def run_server(cfg):
    global config_file_name

    config_file_name = cfg

    thread = threading.Thread(target=consume_messages, args=(cfg,))
    thread.start()

    uvi_cfg = uvicorn.Config(app,
                             host='localhost',
                             port=18022)
    uvi_server = uvicorn.Server(config=uvi_cfg)
    uvi_server.run()



if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", "-c", required=True, action='store', help='the config file for this program')

    parsed, unknown = parser.parse_known_args(sys.argv[1:])

    args = vars(parsed)

    run_server(cfg=args['cfg'])
