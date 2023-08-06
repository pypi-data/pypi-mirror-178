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
                    for row in cur.fetchall():
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

    def create_test_table(self):
        data = [
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Minihamburguesas con papas cajun", "Pechuga de pollo a la plancha", "Tortitas de brócoli", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Ensalada de pepino y tomate", "Porción de elote amarillo", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Carne asada", "Pollo asado", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Chirimol", "Vegetales en mantequilla", "Ensalada fresca", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Deditos de queso", "Pollo horneado", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Ensalada tipo campero", "Ensalada fresca", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Alitas de pollo", "Deditos de pescado", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Ensalada fresca", "Fruta de temporada", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Puré De Papa|arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Hot dog", "Minihamburguesas", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Papas Fritas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Carne en salsa de hongos", "Pasta en salsa Alfredo", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Ensalada de pepino y tomate", "Ensalada fresca", "Fruta de temporada", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Carne asada", "Pollo asado", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Chirimol", "Vegetales en mantequilla", "Ensalada fresca", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Crepas de queso y jamón", "Pollo a la plancha", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Porción de elote amarillo", "Ensalada de pepino y tomate", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Puré De Papa|arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Mini burritos de pollo", "Fajitas de pollo", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Vegetales en mantequilla", "Porción de elote amarillo", "Ensalada fresca", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Carne asada", "Pollo asado", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Chirimol", "Vegetales en mantequilla", "Ensalada fresca", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Pasta con pollo", "Albóndigas de res", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Ensalada fresca", "Fruta de temporada", "Porción de elote amarillo", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Pinchos de pollo", "Enredo", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Ensalada fresca", "Vegetales en mantequilla", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Puré De Papa|arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Tortitas de pollo", "Pasta al gratín", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Deditos De Zanahoria", "Ensalada Fresca", "Puré De Papa|arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Burritos de pollo", "Pollo guisado", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Vegetales en mantequilla", "Porción de elote amarillo", "Ensalada fresca", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Carne asada", "Pollo asado", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Chirimol", "Vegetales en mantequilla", "Ensalada fresca", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Taquitos Pollo empanizado", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Ensalada fresca", "Fruta de temporada", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Puré De Papa|arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Chilaquilas", "Fajitas de pollo", ], "config": {"multi_selection": False}, }, {"title": "Complemento", "options": ["Vegetales en mantequilla", "Porción de elote amarillo", "Ensalada fresca", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Arroz", "Tortillas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
                {"scene": "menu", "pages": [{"title": "Plato principal", "options": ["Hot dog", "Minihamburguesas", ], "config": {"multi_selection": False}, }, {"title": "Acompañamiento", "options": ["Papas Fritas", "Refresco Natural", ], "config": {"multi_selection": True}, }, ]},
        ]
        dates = [
            "14/11/2022",
            "15/11/2022",
            "16/11/2022",
            "17/11/2022",
            "18/11/2022",
            "21/11/2022",
            "22/11/2022",
            "23/11/2022",
            "24/11/2022",
            "25/11/2022",
            "28/11/2022",
            "29/11/2022",
            "30/12/2022",
            "1/12/2022",
            "2/12/2022",
            "5/12/2022",
            "6/12/2022",
            "7/12/2022",
        ]
        values_str = ""
        for i in range(len(data)):
            values_str = values_str + "('" + datetime.datetime.strftime(datetime.datetime.strptime(dates[i], "%d/%m/%Y"), "%Y-%m-%d") + "', '" + json.dumps(data[i]) + "'), \n"
        values_str = values_str[:len(values_str)-3]
        classes = {
            "classes": [
                {
                    "name": "Kinder",
                    "sections": [
                        "1", "2", "3"
                    ]
                },
                {
                    "name": "Preparatoria",
                    "sections": [
                        "1", "2"
                    ]
                },
                {
                    "name": "Primer grado",
                    "sections": [
                        "A", "B", "C"
                    ]
                },
                {
                    "name": "Segundo grado",
                    "sections": [
                        "A", "B"
                    ]
                }
            ]
        }
        commands = [
            {
                "sql": """
                    DROP TABLE IF EXISTS menu;
                """,
                "expects_results": False
            },
            {
                "sql": """
                    CREATE TABLE IF NOT EXISTS menu (
                        menu_id serial PRIMARY KEY,
                        menu_date date NOT NULL,
                        menu_json jsonb NOT NULL
                    );
                """,
                "expects_results": False
            },
            {
                "sql": f"""
                    INSERT INTO menu (menu_date, menu_json)
                    VALUES {values_str}
                    RETURNING menu_date, menu_json;
                """,
                "expects_results": True
            },
            {
                "sql": """
                    DROP TABLE IF EXISTS orders;
                """,
                "expects_results": False
            },
            {
                "sql": """
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id serial PRIMARY KEY,
                        order_placed_date timestamp NOT NULL DEFAULT current_timestamp,
                        ordered_by bigint,
                        ordered_for bigint,
                        order_target_date date,
                        order_notes text,                        
                        order_json jsonb NOT NULL
                    );
                """,
                "expects_results": False
            },
            {
                "sql": """
                    DROP TABLE IF EXISTS guardians CASCADE;
                """,
                "expects_results": False
            },
            {
                "sql": """
                    CREATE TABLE IF NOT EXISTS guardians (
                        guardian_id serial PRIMARY KEY,
                        guardian_created timestamp NOT NULL DEFAULT current_timestamp,
                        guardian_last_updated timestamp NOT NULL DEFAULT current_timestamp,
                        guardian_telegram_id bigint,
                        guardian_phone_number varchar(30) UNIQUE,
                        guardian_first_name varchar(30),
                        guardian_last_name varchar(30),
                        guardian_email text COLLATE pg_catalog."default",
                        guardian_chat_id integer
                    );
                """,
                "expects_results": False
            },
            {
                "sql": f"""
                    INSERT INTO guardians (
                        guardian_phone_number
                    )
                    VALUES 
                    ('50378530273'), 
                    ('50371296561'), 
                    ('50378558010'), 
                    ('50378996740'), 
                    ('50373065764'),
                    ('50372237561'),
                    ('50376017228')
                    RETURNING guardian_id;
                """,
                "expects_results": True
            },
            {
                "sql": """
                    DROP TABLE IF EXISTS consumers;
                """,
                "expects_results": False
            },
            {
                "sql": """
                    CREATE TABLE IF NOT EXISTS consumers (
                        consumer_id serial PRIMARY KEY,
                        consumer_created timestamp NOT NULL DEFAULT current_timestamp,
                        consumer_last_updated timestamp NOT NULL DEFAULT current_timestamp,
                        consumer_guardian_telegram_id bigint,
                        consumer_telegram_id bigint,
                        consumer_phone_number varchar(30),
                        consumer_first_name varchar(30),
                        consumer_last_name varchar(30),
                        consumer_section varchar(30),
                        consumer_class varchar(30),
                        consumer_allergies text,
                        consumer_notes text,
                        consumer_status varchar(30)
                    );
                """,
                "expects_results": False
            },
            {
                "sql": """
                    DROP TABLE IF EXISTS specs;
                """,
                "expects_results": False
            },
            {
                "sql": """
                    CREATE TABLE IF NOT EXISTS specs (
                        spec_id serial PRIMARY KEY,
                        spec_name varchar(30),
                        spec_value jsonb
                    );
                """,
                "expects_results": False
            },
            {
                "sql": f"""
                    INSERT INTO specs (
                        spec_name, spec_value
                    )
                    VALUES 
                    ('classes', '{json.dumps(classes)}')
                    RETURNING spec_id;
                """,
                "expects_results": True
            },
            {
                "sql": """
                    DROP TABLE IF EXISTS prices;
                """,
                "expects_results": False
            },
            {
                "sql": """
                    CREATE TABLE IF NOT EXISTS prices (
                        price_id serial PRIMARY KEY,
                        price_item_name varchar(45) NOT NULL,
                        price_item_value numeric NOT NULL
                    )
                """,
                "expects_results": False
            },
            {
                "sql": f"""
                    INSERT INTO prices (
                        price_item_name, price_item_value
                    )
                    VALUES 
                    ('lunch1', '2.75'),
                    ('lunch2', '3.00'),
                    ('lunch3', '3.25')
                    RETURNING price_id;
                """,
                "expects_results": True
            },
            {
                "sql": """
                    DROP TABLE IF EXISTS transactions;
                """,
                "expects_results": False
            },
            {
                "sql": """
                    CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id serial PRIMARY KEY,
                        guardian_id integer NOT NULL,
                        transaction_id_transaction text COLLATE pg_catalog."default",
                        transaction_client_name text COLLATE pg_catalog."default",
                        transaction_result_transaction text COLLATE pg_catalog."default",
                        transaction_credits numeric NOT NULL,
                        transaction_json jsonb,
                        transaction_type text COLLATE pg_catalog."default",
                        transaction_created timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT transactions_guardian_id_fkey FOREIGN KEY (guardian_id)
                            REFERENCES public.guardians (guardian_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                    )
                """,
                "expects_results": False
            },
            {
                "sql": """
                    DROP TABLE IF EXISTS credits;
                """,
                "expects_results": False
            },
            {
                "sql": """
                    CREATE TABLE IF NOT EXISTS credits (
                        credit_id serial PRIMARY KEY,
                        guardian_id integer NOT NULL,
                        credit_mount numeric NOT NULL,
                        credit_created timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT "FK_Credit_Guardian" FOREIGN KEY (guardian_id)
                            REFERENCES public.guardians (guardian_id) MATCH SIMPLE
                            ON UPDATE NO ACTION
                            ON DELETE NO ACTION
                    )
                """,
                "expects_results": False
            }
        ]
        return self.query_db(commands)

    @staticmethod
    def replace_sql_placeholders(sql_structure_original: [],
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
        