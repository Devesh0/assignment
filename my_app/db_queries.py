import mysql.connector
from mysql.connector import Error
import config


def connect_db(dbname):
    """ Connect to MySQL database """
    try:
        if dbname != config.DATABASE_CONFIG['dbname']:
            raise ValueError("Couldn't find DB with given name")
        conn = mysql.connector.connect(host=config.DATABASE_CONFIG['host'],
                                       user=config.DATABASE_CONFIG['user'],
                                       password=config.DATABASE_CONFIG['password'],
                                       db=config.DATABASE_CONFIG['dbname'])
        return conn

    except Error as e:
        print(e)


my_db = connect_db('codecentral_backup')
db_cursor = my_db.cursor()


def query_fetchall(*args):
    """Common query to fetchall the cursor data."""
    try:
        db_cursor.execute(*args)
        return db_cursor.fetchall()
    except Exception as e:
        print(e)
