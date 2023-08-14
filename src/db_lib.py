import psycopg2 as pg2
from typing import Optional, List, Tuple, Dict


# generic select query
#
def select_query(db: str,
                 schema_table: str,
                 where: Optional[dict] = None,
                 order_by: Optional[list] = None,
                 ascending: Optional[bool] = None) -> Tuple[List[dict], Optional[str]]:

    error = None
    records = []
    sql = f"SELECT * FROM {schema_table}"
    where_values = []
    if where is not None and len(where) > 0:
        sql = f"{sql} where "
        fields = list(where.keys())
        for idx in range(len(fields)):
            field = fields[idx]
            if idx == 0:
                and_operator = ''
            else:
                and_operator = 'AND'
            if isinstance(where[field], list):
                sql = f"{sql} {and_operator} {field} ("
                for value_idx in range(len(where[field])):
                    value = where[field][value_idx]
                    if value_idx == 0:
                        sql = f"{sql} %s"
                    else:
                        sql = f"{sql}, %s"
                    where_values.append(value)
                sql = f"{sql})"
            else:
                sql = f"{sql} {and_operator} {field}%s"
                where_values.append(where[field])

    if order_by is not None and len(order_by) > 0:
        sql = f"{sql} order by "
        for idx in range(len(order_by)):
            field = order_by[idx]
            if idx == 0:
                sql = f"{sql} {field}"
            else:
                sql = f"{sql}, {field}"

        if ascending is not None:
            if ascending:
                sql = f"{sql} ASC"
            else:
                sql = f"{sql} DESC"

    try:

        with pg2.connect(db) as conn:
            if len(where_values) > 0:
                crsr = conn.execute(sql, tuple(where_values))
            else:
                crsr = conn.execute(sql)

            rows = crsr.fetchall()
            meta = crsr.description
            for row in rows:
                record = {meta[col_idx][0]: row[col_idx] for col_idx in range(len(meta))}
                records.append(record)

    except Exception as e:
        error = f"{e}"
    return records, error


# create a table called test_data in schema stack_db
#
def create_test_data_table(db: str) -> Optional[str]:

    error = None
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS stack_db.test_data (
                                                row_id SERIAL PRIMARY KEY,
                                                name TEXT NOT NULL,
                                                age INT NOT NULL,
                                                );
        """
        with pg2.connect(db) as conn:
            conn.execute(sql)
    except Exception as e:
        error = f"{e}"
    return error


# specific select query for test_data table
#
def select_test_data(db: str,
                     where: Optional[dict] = None,
                     order_by: Optional[list] = None,
                     ascending: Optional[bool] = None) -> Tuple[List[dict], Optional[str]]:
    records, error = select_query(db=db,
                                  schema_table='stack_db.test_data',
                                  where=where,
                                  order_by=order_by,
                                  ascending=ascending)
    return records, error


def insert_test_data(db: str,
                     name: str,
                     age: int) -> Tuple[Optional[dict], Optional[str]]:

    record = None
    sql = "INSERT INTO stack_db.test_data (name, age) VALUES(%s, %s)"
    params = (name, age)
    try:
        with pg2.connect(db) as conn:
            conn.execute(sql, params)
        records, error = select_test_data(db=db, where={'name=': name})
        if len(records) > 0:
            record = records[0]
    except Exception as e:
        error = f"{e}"

    return record, error


def configure_db(db: str) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    a function to create the schema and tables of a database
    :param db: the database string to connect to
    :return: tuple containing error
    """
    expected = {'stack_db': {'test_data': create_test_data_table}}
    added_tables = []

    try:
        # create the schema if it doesnt exist
        #
        with pg2.connect(db) as conn:
            crsr = conn.cursor()
            for schema in expected:
                crsr.execute(f"create schema if not exists {schema}")
                conn.commit()
            crsr.close()

        # create the tables if they don't exist
        with pg2.connect(db) as conn:
            crsr = conn.cursor()
            for schema in expected:
                crsr.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema=%s", (schema,))

                # create set of existing tables
                #
                existing_tables = {row[0] for row in crsr.fetchall()}

                # get missing tables by subtracting existing_tables set from expected tables set
                #
                missing_tables = set(expected[schema].keys()) - existing_tables

                for missing_table in missing_tables:
                    # call the function to create the missing table
                    #
                    error = expected[schema][missing_table](db=db)

                    if error is None:
                        added_tables.append(missing_table)
                    else:
                        # if error quit this loop
                        break
            crsr.close()

    except Exception as e:
        error = f"{e}"
        pass

    return added_tables, error


if __name__ == '__main__':

    host = 'localhost'
    port = 5432
    dbname = 'samdb'
    user = 'samdb_user'
    password = 'samdb123'

    db = f"host={host} port={port} dbname={dbname} user={user} password={password}"

    tables_added, error = configure_db(db=db)
    if error is None:
        record, error = insert_test_data(db=db,
                                         name='george',
                                         age=24)
        print(record)

        if error is None:

            records, error = select_test_data(db=db,
                                              where={'name=': 'george'})
            print(records)
