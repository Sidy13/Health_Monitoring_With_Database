import mysql.connector
from mysql.connector import Error
import re

def connect_to_db():
    """Establish a connection to the MySQL database."""
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            port="3306",
            database="health_monitoring",
        )
        print("Connexion to the database established")
        return mydb
    except Error as e:
        print("Connexion error : ", e)
        return None


print("Connexion réussie !")

