
import mysql.connector

def get_connection():

    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Your_Password",
        database="student_analytics",
        use_pure=True,
        connection_timeout=10
    )

    return connection
