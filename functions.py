

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





def connect():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return False

    cursor = mydb.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    query = "SELECT password FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("Login successful")
            return True
        else:
            print("Username or password incorrect")
    else:
        print("Username or password incorrect")

    mydb.close()
    return False


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

    while confirm != "y" and confirm != "n":
        confirm = input("Do you want to continue? [y/n] ").strip().lower()
        if confirm == "y":
            query = "INSERT INTO meals (mealName, calories, mealDate) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, calories, date))
            mydb.commit()
            mydb.close()
            print("Successfully created the meal")
        elif confirm == "n":
            mydb.close()
            print("Operation aborted.")
            return

def modify_meal():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    meal_id = input("Enter the ID of the meal to modify: ").strip()

    new_name = input("Enter the new name of the meal: ").strip()


    while True:
        try:
            new_calories = float(input("Enter the new number of calories for the meal: "))
            if new_calories <= 0:
                raise ValueError("Calories must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input for the calories: {ve}. Please try again.")

    # Obtenir la nouvelle date
    while True:
        date_input = input("Enter the new date of the meal (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(date_input):
            new_date = convert_date(date_input)
            if new_date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")

    print("\nMeal information summary")
    print(f"ID: {meal_id}")
    print(f"Name: {new_name}")
    print(f"Calories: {new_calories}")
    print(f"Date: {new_date}")

    confirm = input("Do you want to continue? [y/n]: ").strip().lower()
    while confirm not in ["y", "n"]:
        confirm = input("Invalid input. Do you want to continue? [y/n]: ").strip().lower()

    if confirm == "y":
        try:
            query = "UPDATE meals SET name = %s, calories = %s, mealDate = %s WHERE mealId = %s"
            cursor.execute(query, (new_name, new_calories, new_date, meal_id))
            mydb.commit()
            print("Successfully updated the meal.")
        except Error as e:
            print("Error during database operation:", e)
        finally:
            mydb.close()
    else:
        mydb.close()
        print("Operation aborted.")

def create_workouts():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    name = input("Enter the name of the workout: ").strip()
    while True:
        duration = int(input("Enter the duration of the workout: ").strip())
        if duration <= 0:
            raise ValueError("Duration cannot be less than 0")
        break
    while True:
        calories = float(input("Enter the number of calories burned during the workout: "))
        if calories <= 0:
            raise ValueError("Calories cannot be less than 0")
        break
    while True:
        date_input = input("Enter the date of the workout (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(date_input):
            date = convert_date(date_input)
            if date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")
    print("\nWorkout informations summary")
    print("Name: ", name)
    print("Calories: ", calories)
    print("Date: ", date)
    confirm = input("Do you want to continue? [y/n] ").strip().lower()
    while confirm != "y" and confirm != "n":
        confirm = input("Do you want to continue? [y/n] ").strip().lower()
        if confirm == "y":
            query = "INSERT INTO workouts (workoutName, caloriesBurned, wourkoutDate) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, calories, date))
            mydb.commit()
            mydb.close()
            print("Successfully created the workout")
            break
        elif confirm == "n":
            mydb.close()
            print("Operation aborted.")
            return

def modify_workouts():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    workout_id = input("Enter the ID of the workout to modify: ").strip()

    new_name = input("Enter the new name of the workout: ").strip()

    while True:
        try:
            new_duration = int(input("Enter the new duration of the workout (in minutes): ").strip())
            if new_duration <= 0:
                raise ValueError("Duration must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input for the duration: {ve}. Please try again.")

    while True:
        try:
            new_calories = float(input("Enter the new number of calories burned during the workout: "))
            if new_calories <= 0:
                raise ValueError("Calories burned must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input for the calories burned: {ve}. Please try again.")

    while True:
        date_input = input("Enter the new date of the workout (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(date_input):
            new_date = convert_date(date_input)
            if new_date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")

    print("\nWorkout information summary")
    print(f"ID: {workout_id}")
    print(f"Name: {new_name}")
    print(f"Duration: {new_duration} minutes")
    print(f"Calories burned: {new_calories}")
    print(f"Date: {new_date}")

    confirm = input("Do you want to continue? [y/n]: ").strip().lower()
    while confirm not in ["y", "n"]:
        confirm = input("Invalid input. Do you want to continue? [y/n]: ").strip().lower()

    if confirm == "y":
        try:
            query = "UPDATE workouts SET workoutName = %s, duration = %s, caloriesBurned = %s, workoutDate = %s WHERE id = %s"
            cursor.execute(query, (new_name, new_duration, new_calories, new_date, workout_id))
            mydb.commit()
            print("Successfully updated the workout.")
        except Error as e:
            print("Error during database operation:", e)
        finally:
            mydb.close()
    else:
        mydb.close()
        print("Operation aborted.")


def create_sleep():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    while True:
        date_input = input("Enter the date of the sleep: ").strip()
        if validate_date(date):
            date = convert_date(date_input)
            if date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")
    sleepQuality = input("Enter the quality of your sleep: ").strip()
    while True:
        duration = int(input("Enter the duration of your sleep: "))
        if duration <= 0:
            raise ValueError("Duration cannot be less than 0")
        break
    print("\nSleep informations summary")
    print("Date: ", date)
    print("Quality: ", sleepQuality)
    print("Duration: ", duration)
    confirm = input("Do you want to continue? [y/n] ").strip().lower()
    while confirm != "y" and confirm != "n":
        confirm = input("Do you want to continue? [y/n] ").strip().lower()
        if confirm == "y":
            query = "INSERT INTO sleeps (durationInHours, sleepQuality, date) VALUES (%s, %s, %s)"
            cursor.execute(query, (duration, sleepQuality, date))
            mydb.commit()
            mydb.close()
            print("Successfully created the sleep")
            break
        elif confirm == "n":
            mydb.close()
            print("Operation aborted.")
            return

def modify_sleep():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        current_date_input = input("Enter the date of the sleep to modify (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(current_date_input):
            current_date = convert_date(current_date_input)
            if current_date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")

    while True:
        new_date_input = input("Enter the new date of the sleep (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(new_date_input):
            new_date = convert_date(new_date_input)
            if new_date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")

    sleep_quality = input("Enter the quality of your sleep: ").strip()

    while True:
        try:
            duration = int(input("Enter the duration of your sleep (in hours): "))
            if duration <= 0:
                raise ValueError("Duration must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please try again.")

    print("\nSleep informations summary")
    print(f"Current Date: {current_date}")
    print(f"New Date: {new_date}")
    print(f"Quality: {sleep_quality}")
    print(f"Duration: {duration} hours")

    confirm = input("Do you want to continue? [y/n]: ").strip().lower()
    while confirm not in ["y", "n"]:
        confirm = input("Invalid input. Do you want to continue? [y/n]: ").strip().lower()

    if confirm == "y":
        try:
            query = "UPDATE sleep SET duration = %s, quality = %s, date = %s WHERE date = %s"
            cursor.execute(query, (duration, sleep_quality, new_date, current_date))
            mydb.commit()
            print("Successfully updated the sleep record.")
        except Error as e:
            print("Error during database operation:", e)
        finally:
            mydb.close()
    else:
        mydb.close()
        print("Operation aborted.")











