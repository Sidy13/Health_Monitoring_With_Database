

import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime
import bcrypt

def connect_to_db():
    #Establish a connection to the MySQL database
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



def validate_date(date):
    #Validate date format (DD-MM-YYYY)
    try:
        date = date.replace("/", "-")
        datetime.strptime(date, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def convert_date(date):
    #Convert date from DD-MM-YYYY or DD/MM/YYYY to YYYY-MM-DD
    try:
        date = date.replace("/", "-")
        return datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def create_user():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    username = input("Enter your username: ")
    firstName = input("Enter your first name: ")
    lastName = input("Enter your last name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    print("\nYour informations summary")
    print("username: ", username)
    print("first name: ", firstName)
    print("last name: ", lastName)
    print("email: ", email)
    confirm = input("Do you want to continue? [y/n] ").strip().lower()
    if confirm == "y":
        query = "Insert into user (username, firstName, lastName, password, email) values (%s, %s, %s, %s, %s)"
        cursor.execute(query, (username, firstName, lastName, hashed_password, email))
        mydb.commit()
        mydb.close()
        print("User created successfully")
    else:
        mydb.close()
        print("User aborted")



def create_meal():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    name = input("Enter the name of the meal: ").strip()
    while True:
        try:
            calories = float(input("Enter the number of calories of the meal: "))
            if calories <= 0:
                raise ValueError("Calories cannot be less than 0")
            break
        except ValueError:
            print("Invalid input for the calories, please try again")
    while True:
        date_input = input("Enter the date of the meal (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(date_input):
            date = convert_date(date_input)
            if date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")

    print("\nMeal informations summary")
    print("Name: ", name)
    print("Calories: ", calories)
    print("Date: ", date)
    confirm = input("Do you want to continue? [y/n] ").strip().lower()
    if confirm == "y":
        query = "INSERT INTO meals (mealName, calories, mealDate) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, calories, date))
        mydb.commit()
        mydb.close()
        print("Successfully created the meal")
    else:
        mydb.close()
        print("Operation aborted.")
        return
