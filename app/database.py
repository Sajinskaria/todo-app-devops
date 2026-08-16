
import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "todo_user"),
            password=os.getenv("DB_PASSWORD", "todo_password"),
            database=os.getenv("DB_NAME", "todo_db")
        )

        return connection

    except Error as error:
        print(f"Database connection error: {error}")
        return None
