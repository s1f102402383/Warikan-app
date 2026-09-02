import os
import pymysql

mariadb_host = os.getenv("MYSQL_HOST", "mariadb")
mariadb_user = os.getenv("MYSQL_USER", "user")
mariadb_password = os.getenv("MYSQL_PASSWORD", "password")


def get_db_connection():
    """DB接続を取得する"""
    conn = pymysql.connect(
        host=mariadb_host, user=mariadb_user, password=mariadb_password
    )
    return conn
