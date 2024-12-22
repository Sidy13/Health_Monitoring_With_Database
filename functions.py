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

def validate_date(date):
    """Validate date format (YYYY-MM-DD)."""
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date))


def create_meal():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    name = input("Enter the name of the meal").strip()
    while True:
        try:
            calories = float(input("Enter the number of calories of the meal: "))
            if calories <= 0:
                raise ValueError("Calories cannot be less than 0")
            break
        except ValueError:
            print("Invalid input for the calories, please try again")
    while True:
        date = input("Enter the date of the meal: ").strip()
        if validate_date(date):
            break
        print("Invalid date format, enter it within the format YYYY-MM-DD")
    print("\nInformations summary")
    print("Name: ", name)
    print("Calories: ", calories)
    print("Date: ", date)
    confirm = input("Do you want to continue? [y/n] ").strip().lower()
    if confirm == "y":
        query = "INSERT INTO meals (name, calories, date) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, calories, date))
        mydb.commit()
        mydb.close()
        print("Successfully created the meal")
    else:
        mydb.close()
        print("Operation aborted.")
        return
