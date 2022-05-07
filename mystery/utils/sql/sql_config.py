"""
Read conf/db_config.ini and connect to database
"""

import configparser
import os
import pymysql


def get_db_config():
    """
    Get db config from conf/db_config.ini
    """
    root_dir = os.getcwd()  # /home/hohin/mystery
    # root_dir = os.path.dirname(os.path.abspath('..'))
    config_path = os.path.join(root_dir, "conf/db_config.ini")
    # print(config_path)
    config = configparser.ConfigParser()
    config.read(config_path)

    return config


def get_db_conn():
    """
    Get db connection
    """
    try:
        config = get_db_config()

        conn = pymysql.connect(host=config['Mysql-Database']['HOST'],
                               port=int(config['Mysql-Database']['PORT']),
                               user=config['Mysql-Database']['USER'],
                               password=config['Mysql-Database']['PASSWORD'],
                               db=config['Mysql-Database']['DATABASE'],
                               charset=config['Mysql-Database']['CHARSET'])
        return conn
    except Exception as e:
        print(e)
        print("Database connection failed")


def get_db_cursor(conn):
    """
    Get db cursor
    """
    try:
        cursor = conn.cursor()
        return cursor
    except Exception as e:
        print(e)
        print("Database cursor failed")


def get_db_conn_cursor():
    """
    Get db connection and cursor
    """
    try:
        conn = get_db_conn()
        cursor = get_db_cursor(conn)
        return conn, cursor
    except Exception as e:
        print(e)
        print("Database connection failed")


def close_db_conn(conn):
    """
    Close db connection
    """
    conn.close()


def close_db_cursor(cursor):
    """
    Close db cursor
    """
    cursor.close()


def close_db_conn_cursor(conn, cursor):
    """
    Close db connection and cursor
    """
    close_db_cursor(cursor)
    close_db_conn(conn)


def connect_db_test():
    """
    Test db connection
    """
    try:
        conn = get_db_conn()
        cursor = get_db_cursor(conn)
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print("Database version : %s " % data)
        print("Database connection successful")
        close_db_conn_cursor(conn, cursor)
    except Exception as e:
        print(e)
        print("Database connection failed")
