import os
import pymysql


# MariaDBの接続情報
mariadb_host = os.getenv(
    "MYSQL_HOST",
    "mariadb"
)

mariadb_user = os.getenv(
    "MYSQL_USER",
    "user"
)

mariadb_password = os.getenv(
    "MYSQL_PASSWORD",
    "password"
)

mariadb_database = os.getenv(
    "MYSQL_DATABASE",
    "mydb"
)


def get_db_connection():
    """MariaDBへの接続を取得する"""

    conn = pymysql.connect(
        host=mariadb_host,
        user=mariadb_user,
        password=mariadb_password,
        database=mariadb_database,
        charset="utf8mb4"
    )

    return conn