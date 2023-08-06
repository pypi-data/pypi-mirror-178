import json

import psycopg2
import logging
from logging import config
import datetime
from typing import Union
import copy

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DataSource:
    def __init__(self, database_url):
        self.database_url = database_url

    def get_connection(self):
        logger.debug("Entering function")
        return psycopg2.connect(self.database_url, sslmode='allow')

    @staticmethod
    def close_connection(conn):
        logger.debug("Entering function")
        if conn is not None:
            conn.close()

    def query_db(self, commands: list, parameters: list = None) -> list:
        logger.debug("Entering function")
        all_results = list()
        conn = None
        command = dict()
        command["sql"] = ""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            command_results = list()
            for command in commands:
                if parameters is not None:
                    parameter = parameters[commands.index(command)]
                    if parameter is not None:
                        logger.debug(f"Executing query:\nsql: {command['sql']}\nparameters: {parameter}")
                        cur.execute(command["sql"], parameter)
                    else:
                        logger.debug(f"Executing query:\nsql: {command['sql']}\nparameters: {parameter}")
                        cur.execute(command["sql"])
                else:
                    logger.debug(f"Executing query:\nsql: {command['sql']}\nparameters: None")
                    cur.execute(command["sql"])
                conn.commit()
                if command["expects_results"]:
                    logger.debug(f"query expects results")
                    c = 0
                    query_results = cur.fetchall()
                    logger.debug(f"query_results: {query_results}")
                    for row in query_results:
                        command_results.append(row)
                        c = c + 1
                    logger.debug(f"query returned {c} rows")
                all_results.append(command_results)
            cur.close()
            logger.debug(f"query executed successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            logger.exception(error)
            logger.error(command["sql"])
            logger.error(parameters)
            raise error
        finally:
            self.close_connection(conn)
            return all_results

    @staticmethod
    def parse_query(query_result: list, query_index: int, record_index: int,
                    field_index: int):
        logger.debug("Entering function")
        result = None
        if len(query_result) > 0:
            if query_index < len(query_result):
                if record_index < len(query_result[query_index]):
                    if field_index < len(query_result[query_index][record_index]):
                        result = query_result[query_index][record_index][field_index]
        return result

    @staticmethod
    def data_exists(data) -> bool:
        logger.debug("Entering function")
        result = False
        if data is not None:
            if data != "":
                result = True
        return result

    @staticmethod
    def replace_sql_placeholders(sql_structure_original: list,
                                 table_name: Union[list[str], None] = None,
                                 column_list: Union[list[str], None] = None,
                                 return_list: Union[list[str], None] = None,
                                 update_list: Union[list[str], None] = None):
        logger.debug("Entering function")
        logger.debug(f"table_name: {table_name}")
        logger.debug(f"column_list: {column_list}")
        logger.debug(f"return_list: {return_list}")
        logger.debug(f"update_list: {update_list}")
        print(type(table_name))
        index = 0
        sql_structure_new = copy.deepcopy(sql_structure_original)
        for item in sql_structure_new:
            logger.debug(f"item: {item}")
            sql = item["sql"]
            logger.debug(f"sql: {sql}")
            if table_name is not None:
                sql = sql.replace("<table_name>", table_name[index])
                logger.debug(f"sql after replacing <table_name>: {sql}")
            if column_list is not None:
                sql = sql.replace("<column_list>", column_list[index])
                logger.debug(f"sql after replacing <column_list>: {sql}")
            if return_list is not None:
                sql = sql.replace("<return_list>", return_list[index])
                logger.debug(f"sql after replacing <return_list>: {sql}")
            if update_list is not None:
                sql = sql.replace("<update_list>", update_list[index])
                logger.debug(f"sql after replacing <update_list>: {sql}")
            item["sql"] = sql
            logger.debug(f"new item after replacing sql: {item}")
            sql_structure_new[sql_structure_new.index(item)] = item
            logger.debug(f"new sql_structure_new after replacing item: {sql_structure_new}")
            index = index + 1
        return sql_structure_new

    def query_one_datum(self, sql: str, value_if_none=[]):
        logger.debug("Entering function")
        query_result = self.query_db([{"sql": sql, "expects_results": True}])
        logger.debug(f"query_result: {query_result}")
        parsed_result = self.parse_query(query_result, 0, 0, 0)
        logger.debug(f"parsed_result: {parsed_result}")
        if not self.data_exists(parsed_result):
            output = value_if_none
        else:
            output = parsed_result
        logger.debug(f"output: {output}")
        return output

    def query_one_list(self, sql: str, value_if_none=[]):
        logger.debug("Entering function")
        query_result = self.query_db([{"sql": sql, "expects_results": True}])
        logger.debug(f"query_result: {query_result}")
        if query_result is not None:
            if len(query_result[0]) == 1 and len(query_result[0][0]) == 1 and query_result[0][0][0] is None:
                output = value_if_none
            else:
                output = self.query_list_to_list(query_result[0])
        else:
            output = value_if_none
        logger.debug(f"output: {output}")
        return output

    def query_one_record(self, sql: str, value_if_none=[]):
        logger.debug("Entering function")
        query_result = self.query_db([{"sql": sql, "expects_results": True}])
        logger.debug(f"query_result: {query_result}")
        if query_result is not None:
            if len(query_result[0]) == 1 and len(query_result[0][0]) == 1 and query_result[0][0][0] is None:
                output = value_if_none
            else:
                output = query_result[0]
        else:
            output = value_if_none
        logger.debug(f"output: {output}")
        return output

    @staticmethod
    def query_list_to_text(query_list: list, separator: str, default_if_output_empty: str) -> str:
        output = ""
        if type(query_list) == list or type(query_list) == tuple:
            for item in query_list:
                if type(item) == list or type(item) == tuple:
                    for item2 in item:
                        if type(item2) == list or type(item2) == tuple:
                            for item3 in item2:
                                output = output + str(item3)
                                if item2.index(item3) < len(item2) - 1:
                                    output = output + separator
                        else:
                            output = output + str(item2)
                            if item.index(item2) < len(item) - 1:
                                output = output + separator
                else:
                    output = output + str(item)
                    if query_list.index(item) < len(query_list) - 1:
                        output = output + separator
        else:
            output = str(query_list)
        if output == "":
            output = default_if_output_empty
        return output

    @staticmethod
    def query_list_to_list(query_list: list):
        output = list()
        if type(query_list) == list or type(query_list) == tuple:
            for item in query_list:
                if type(item) == list or type(item) == tuple:
                    for item2 in item:
                        if type(item2) == list or type(item2) == tuple:
                            for item3 in item2:
                                output.append(item3)
                        else:
                            output.append(item2)
                else:
                    output.append(item)
        else:
            output.append(query_list)
        return output
