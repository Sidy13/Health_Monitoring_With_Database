import mysql.connector
from mysql.connector import Error
from datetime import datetime
import bcrypt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import re

#Helper
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

def reverse_convert_date(date):
    try:
        date = date.replace("/", "-")
        return datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
    except ValueError:
        return None
#User
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
    height = int(input("Enter your height in cm: "))
    height_in_meters = height / 100
    weight = int(input("Enter your weight: "))
    BMI = weight / (height_in_meters ** 2)
    password = input("Enter your password: ")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    print("\nYour informations summary")
    print("username: ", username)
    print("first name: ", firstName)
    print("last name: ", lastName)
    print("email: ", email)
    print("height: ", height)
    print("weight: ", weight)
    confirm = input("Do you want to continue? [y/n] ").strip().lower()
    if confirm == "y":
        query = "Insert into user (username, firstName, lastName, password, email, height, weight, bmi) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (username, firstName, lastName, hashed_password, email, height, weight, BMI))
        mydb.commit()
        mydb.close()
        print("User created successfully")
    else:
        mydb.close()
        print("User aborted")

def login():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return False, None

    cursor = mydb.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    query = "SELECT password FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user_id, result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("Login successful")
            return True, user_id
        else:
            print("Username or password incorrect")
    else:
        print("Username or password incorrect")

    mydb.close()
    return False, None

def modify_user():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    print("In order to modify your account, you must login again.")
    is_logged_in, user_id = login()
    if is_logged_in:
        username = input("Enter your username: ")
        firstName = input("Enter your first name: ")
        lastName = input("Enter your last name: ")
        email = input("Enter your email: ")
        height = int(input("Enter your height: "))
        weight = int(input("Enter your weight: "))
        BMI = weight / (height ** 2)
        password = input("Enter your password: ")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE user SET username = %s, firstName = %s, lastName = %s, email = %s, password = %s height = %s, weight = %s, bmi = %s WHERE userId = %s"
        query2 = "UPDATE user SET height = %s, weight = %s, bmi = %s WHERE userId = %s"
        cursor.execute(query, (username, firstName, lastName, email, hashed_password, user_id ))
        cursor.execute(query2, (height, weight, BMI, user_id, ))
        print("User updated successfully")
        mydb.commit()
        mydb.close()

def delete_user():
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    print("In order to delete your account, you must login again.")
    is_logged_in, user_id = login()
    if is_logged_in:
        choice = input("Are you sure you want to delete this account ? [y/n] ").strip().lower()
        while (choice != "y" and choice != "n"):
            choice = input("Are you sure you want to delete this account ? [y/n] ").strip().lower()
        if choice == "y":
            query = "DELETE FROM user WHERE userId = %s"
            cursor.execute(query, (user_id, ))
            mydb.commit()
            mydb.close()
            print("User deleted successfully, sorry to see you leave")
            return
        else:
            mydb.close()
            print("Operation aborted")
            return

def explain_BMI(BMI):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    if BMI<0:
        print("BMI cannot be negative")
        return
    elif BMI < 18.5:
        print("Your BMI is equal to ", BMI," which classify you as an underweight")
    elif 18.5 <= BMI < 25:
        print("Your BMI is equal to ", BMI," which classify you as a normal")
    elif 25 <= BMI < 30:
        print("Your BMI is equal to ", BMI," which classify you as a overweight")
    elif 30 <= BMI < 35:
        print("Your BMI is equal to ", BMI," which classify you as a first class obese")
    elif 35 <= BMI < 40:
        print("Your BMI is equal to ", BMI," which classify you as a second class obese")
    elif BMI >= 40:
        print("Your BMI is equal to ", BMI," which classify you as a third class obese")


def display_user(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    try:
        query = "SELECT * FROM user WHERE userId = %s"
        cursor.execute(query, (user_id, ))
        user = cursor.fetchone()
        if user:
            print("\n User information :")
            print("username: ", user[1])
            print("first name: ", user[2])
            print("last name: ", user[3])
            print("email: ", user[5])
            print("height: ", user[7])
            print("weight: ", user[6])
            bmi = user[8]
            print("bmi: ", explain_BMI(bmi))
    except Error as e:
        print(e)
        return





#Meal
def create_meal(user_id):
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
            query = "INSERT INTO meals (mealName, calories, mealDate, userId) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, calories, date, user_id))
            mydb.commit()
            mydb.close()
            print("Successfully created the meal")
        elif confirm == "n":
            mydb.close()
            print("Operation aborted.")
            return

def modify_meal(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    meal_id = int(input("Enter the meal ID: "))

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
            query = "UPDATE meals SET name = %s, calories = %s, mealDate = %s WHERE mealId = %s and userId = %s"
            cursor.execute(query, (new_name, new_calories, new_date, meal_id, user_id))
            mydb.commit()
            print("Successfully updated the meal.")
        except Error as e:
            print("Error during database operation:", e)
        finally:
            mydb.close()
    else:
        mydb.close()
        print("Operation aborted.")

def display_meal_by_id(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    # Demander l'ID du repas
    while True:
        try:
            meal_id = int(input("Enter the meal ID: ").strip())
            if meal_id <= 0:
                raise ValueError("Meal ID must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please try again.")

    # Exécuter la requête
    try:
        query = "SELECT * FROM meals WHERE mealId = %s AND userId = %s"
        cursor.execute(query, (meal_id,user_id))
        meal = cursor.fetchone()

        # Vérifier si un repas a été trouvé
        if meal:
            print("\nMeal Information:")
            print(f"ID: {meal[0]}, Name: {meal[1]}, Calories: {meal[2]}, Date: {meal[3]}")
        else:
            print(f"No meal found with ID {meal_id}.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_meal_by_name(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    meal_name = input("Enter the meal name: ").strip()

    try:
        query = "SELECT * FROM meals WHERE mealName = %s AND userId = %s"
        cursor.execute(query, (meal_name, user_id))
        meals = cursor.fetchall()

        # Vérifier si des repas ont été trouvés
        if meals:
            print(f"\nMeals matching the name '{meal_name}':")
            for meal in meals:
                print(f"ID: {meal[0]}, Name: {meal[1]}, Calories: {meal[2]}, Date: {meal[3]}")
        else:
            print(f"No meals found with the name '{meal_name}'.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_meal_by_calories(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        try:
            calories = float(input("Enter the minimum number of calories: ").strip())
            if calories <= 0:
                raise ValueError("Calories must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please try again.")

    try:
        query = "SELECT * FROM meals WHERE calories >= %s AND userId ORDER BY calories ASC"
        cursor.execute(query, (calories,user_id))
        meals = cursor.fetchall()

        if meals:
            print("\nMeals with at least", calories, "calories:")
            for meal in meals:
                print(f"ID: {meal[0]}, Name: {meal[1]}, Calories: {meal[2]}, Date: {meal[3]}")
        else:
            print(f"No meals found with at least {calories} calories.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_meal_by_date(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        date_input = input("Enter the date (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(date_input):
            date = convert_date(date_input)
            if date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")

    try:
        query = "SELECT * FROM meals WHERE mealDate >= %s and userId = %s ORDER BY mealDate ASC"
        cursor.execute(query, (date,user_id))
        meals = cursor.fetchall()

        if meals:
            print(f"\nMeals from {date} onwards (sorted by date):")
            for meal in meals:
                print(f"ID: {meal[0]}, Name: {meal[1]}, Calories: {meal[2]}, Date: {meal[3]}")
        else:
            print(f"No meals found from {date} onwards.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_all_meals(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    query = "SELECT * FROM meals where userId = %s "
    cursor.execute(query, (user_id,))
    meals = cursor.fetchall()
    if meals:
        print("\nMeals:")
        for meal in meals:
            print(f"ID: {meal[0]}, Name: {meal[1]}, Calories: {meal[2]}, Date: {meal[3]}")
        mydb.close()
    else:
        print("No meals found.")
        mydb.close()

def display_meals(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    while True:
        choice = int(input("How do you want to see the meal ? : \n1. By id \n2. By name \n3. By number of calories \n4. By date \n5. Show all meals \nEnter a number"))
        while choice not in [1, 2, 3, 4, 5]:
            print("Invalid input. Please try again.")
            choice = int(input("Enter the choice number: "))
        if choice == 1:
            display_meal_by_id(user_id)
        elif choice == 2:
            display_meal_by_name(user_id)
        elif choice == 3:
            display_meal_by_calories(user_id)
        elif choice == 4:
            display_meal_by_date(user_id)
        elif choice == 5:
            display_all_meals(user_id)

def delete_meal(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    try:
        meal_id = int(input("Enter the ID of the meal you would like to delete: "))
        if meal_id <= 0:
            raise ValueError("Meal ID must be greater than 0.")
        query_check = "SELECT * FROM meals WHERE mealId = %s AND userId = %s"
        cursor.execute(query_check, (meal_id,user_id))
        meal = cursor.fetchone()
        if not meal:
            print("\nMeal does not exist.")
            return
        mealName = meal[1]
        mealDate = meal[3]
        mealDate = reverse_convert_date(mealDate)

        while True:
            confirm = input(f"\nDo you want to delete the {mealName} from the {mealDate} ? (y/n): ").lower().strip()
            if confirm in ["y", "n"]:
                break
            print("Invalid input. Please enter 'y' or 'n'.")

        if confirm == "y":
            query = "DELETE FROM meals WHERE mealId = %s AND userId = %s"
            cursor.execute(query, (meal_id, user_id))
            mydb.commit()
            print("\nMeal has been deleted.")
        else:
            print("\nMeal was not deleted.")
        mydb.close()
    except ValueError as ve:
        print(f"Invalid input: {ve}. Please try again.")
    except Error as e:
        print("Error during database operation:", e)


def manage_meals(user_id):
    print("\nMeal Management")
    print("1. Create Meal")
    print("2. Modify Meal")
    print("3. Display Meals")
    print("4. Delete Meal")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        create_meal(user_id)
    elif choice == 2:
        modify_meal(user_id)
    elif choice == 3:
        display_meals(user_id)
    elif choice == 4:
        delete_meal(user_id)
    else:
        print("Invalid choice.")

#Workouts
def create_workouts(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    name = input("Enter the name of the workout: ").strip()
    while True:
        duration = int(input("Enter the duration in minutes of the workout: ").strip())
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
            query = "INSERT INTO workouts (workoutName, durationInMinutes, caloriesBurned, wourkoutDate, userId) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query, (name, duration, calories, date, user_id))
            mydb.commit()
            mydb.close()
            print("Successfully created the workout")
            break
        elif confirm == "n":
            mydb.close()
            print("Operation aborted.")
            return

def modify_workouts(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    workout_id = int(input("Enter the workout ID: "))

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
            query = "UPDATE workouts SET workoutName = %s, duration = %s, caloriesBurned = %s, workoutDate = %s WHERE workoutId = %s and userId = %s;"
            cursor.execute(query, (new_name, new_duration, new_calories, new_date, workout_id, user_id))
            mydb.commit()
            print("Successfully updated the workout.")
        except Error as e:
            print("Error during database operation:", e)
        finally:
            mydb.close()
    else:
        mydb.close()
        print("Operation aborted.")

def display_workout_by_id(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        try:
            workout_id = int(input("Enter the workout ID: ").strip())
            if workout_id <= 0:
                raise ValueError("Workout ID must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please try again.")

    try:
        query = "SELECT * FROM workouts WHERE workoutId = %s AND userId = %s;"
        cursor.execute(query, (workout_id,user_id))
        workout = cursor.fetchone()

        if workout:
            print("\nWorkout Information:")
            print(f"ID: {workout[0]}, Name: {workout[1]}, Duration: {workout[2]} minutes, "
                  f"Calories Burned: {workout[3]}, Date: {workout[4]}")
        else:
            print(f"No workout found with ID {workout_id}.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_workout_by_name(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    workout_name = input("Enter the workout name: ").strip()

    try:
        query = "SELECT * FROM workouts WHERE workoutName = %s and userId = %s;"
        cursor.execute(query, (workout_name,))
        workouts = cursor.fetchall()

        if workouts:
            print(f"\nWorkouts matching the name '{workout_name}':")
            for workout in workouts:
                print(f"ID: {workout[0]}, Name: {workout[1]}, Duration: {workout[2]} minutes, "
                      f"Calories Burned: {workout[3]}, Date: {workout[4]}")
        else:
            print(f"No workouts found with the name '{workout_name}'.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_workout_by_date(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        date_input = input("Enter the date (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(date_input):
            date = convert_date(date_input)
            if date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")

    try:
        query = "SELECT * FROM workouts WHERE workoutDate >= %s and userId = %s ORDER BY workoutDate ASC"
        cursor.execute(query, (date,user_id))
        workouts = cursor.fetchall()

        if workouts:
            print(f"\nWorkouts from {date} onwards (sorted by date):")
            for workout in workouts:
                print(f"ID: {workout[0]}, Name: {workout[1]}, Duration: {workout[2]} minutes, "
                      f"Calories Burned: {workout[3]}, Date: {workout[4]}")
        else:
            print(f"No workouts found from {date} onwards.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_workout_by_calories(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        try:
            min_calories = float(input("Enter the minimum number of calories burned: ").strip())
            if min_calories <= 0:
                raise ValueError("Calories burned must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please try again.")

    try:
        query = "SELECT * FROM workouts WHERE caloriesBurned >= %s and userId = %s ORDER BY caloriesBurned ASC"
        cursor.execute(query, (min_calories,user_id))
        workouts = cursor.fetchall()

        if workouts:
            print(f"\nWorkouts burning at least {min_calories} calories (sorted by calories burned):")
            for workout in workouts:
                print(f"ID: {workout[0]}, Name: {workout[1]}, Duration: {workout[2]} minutes, "
                      f"Calories Burned: {workout[3]}, Date: {workout[4]}")
        else:
            print(f"No workouts found burning at least {min_calories} calories.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_all_workouts(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    query = "SELECT * FROM workout where userId = %s ORDER BY workoutDate ASC"
    cursor.execute(query, (user_id,))
    workouts = cursor.fetchall()
    if workouts:
        print(f"\nAll workouts:")
        for workout in workouts:
            print(f"ID: {workout[0]}, Name: {workout[1]}, Duration: {workout[2]} minutes, "
                  f"Calories Burned: {workout[3]}, Date: {workout[4]}")
    else:
        print(f"No workouts found.")
    mydb.close()

def display_workouts(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    choice = int(input("How do you want to see the workouts? \n1. By id \n2. By name \n3. By date \n4. By calories burned \n5. Show all workouts "))
    while choice not in [1, 2, 3, 4, 5]:
        print("Invalid input. Please try again.")
        choice = int(input("Enter the choice number: "))
    if choice == 1:
        display_workout_by_id(user_id)
    if choice == 2:
        display_workout_by_name(user_id)
    elif choice == 3:
        display_workout_by_date(user_id)
    elif choice == 4:
        display_workout_by_calories(user_id)
    elif choice == 5:
        display_all_workouts(user_id)

def delete_workout(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    try:
        workoutId = int(input("Enter the ID of the workout you would like to delete: "))
        if workoutId <= 0:
            raise ValueError("Workout ID must be greater than 0.")
        cursor = mydb.cursor()
        query_check = "SELECT * FROM workouts WHERE userId = %s AND workoutID = %s"
        cursor.execute(query_check, (user_id,workoutId))
        workouts = cursor.fetchone()
        if not workouts:
            print("No workouts with ID ",workoutId," found.")
            return
        workoutName = workouts[1]
        workoutDate = workouts[4]
        workoutDate = reverse_convert_date(workoutDate)
        while True:
            confirm = input(f"\nDo you want to delete the {workoutName} from the {workoutDate} ? (y/n):").lower().strip()
            if confirm in ["y", "n"]:
                break
            print("Invalid input. Please enter 'y' or 'n'.")

        if confirm == "y":
            query = "DELETE FROM workouts WHERE workoutId = %s AND userId = %s"
            cursor.execute(query, (workoutId, user_id))
            mydb.commit()
            print("\nMeal has been deleted.")
        else:
            print("\nMeal was not deleted.")
    except ValueError as ve:
        print(f"Invalid input: {ve}. Please try again.")
    except Error as e:
        print("Error during database operation:", e)


def manage_workouts(user_id):
    print("\nWorkout Management")
    print("1. Create Workout")
    print("2. Modify Workout")
    print("3. Display Workouts")
    print("4. Delete Workout")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        create_workouts(user_id)
    elif choice == 2:
        modify_workouts(user_id)
    elif choice == 3:
        display_workouts(user_id)
    elif choice == 4:
        delete_workout(user_id)
    else:
        print("Invalid choice.")

#Sleep
def create_sleep(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    while True:
        date_input = input("Enter the date of the sleep: ").strip()
        if validate_date(date_input):
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
            query = "INSERT INTO sleeps (durationInHours, sleepQuality, date, userId) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (duration, sleepQuality, date, user_id))
            mydb.commit()
            mydb.close()
            print("Successfully created the sleep")
            break
        elif confirm == "n":
            mydb.close()
            print("Operation aborted.")
            return

def modify_sleep(user_id):
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
            query = "UPDATE sleep SET duration = %s, quality = %s, date = %s WHERE date = %s and userId = %s;"
            cursor.execute(query, (duration, sleep_quality, new_date, current_date, user_id))
            mydb.commit()
            print("Successfully updated the sleep record.")
        except Error as e:
            print("Error during database operation:", e)
        finally:
            mydb.close()
    else:
        mydb.close()
        print("Operation aborted.")

def display_sleep_by_id(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        try:
            sleep_id = int(input("Enter the sleep ID: ").strip())
            if sleep_id <= 0:
                raise ValueError("Sleep ID must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please try again.")

    try:
        query = "SELECT * FROM sleep WHERE sleepId = %s and userId = %s;"
        cursor.execute(query, (sleep_id,user_id))
        sleep_entry = cursor.fetchone()

        if sleep_entry:
            print("\nSleep Information:")
            print(f"ID: {sleep_entry[0]}, Date: {sleep_entry[1]}, Quality: {sleep_entry[2]}, Duration: {sleep_entry[3]} hours")
        else:
            print(f"No sleep entry found with ID {sleep_id}.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_sleep_by_date(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        date_input = input("Enter the date (DD-MM-YYYY or DD/MM/YYYY): ").strip()
        if validate_date(date_input):
            date = convert_date(date_input)
            if date:
                break
        print("Invalid date format. Please enter it in the format DD-MM-YYYY or DD/MM/YYYY.")

    try:
        query = "SELECT * FROM sleep WHERE sleepDate = %s and userId = %s ORDER BY sleepDate ASC"
        cursor.execute(query, (date, user_id))
        sleep_entries = cursor.fetchall()

        if sleep_entries:
            print(f"\nSleep entries from {date}")
            for sleep in sleep_entries:
                print(f"ID: {sleep[0]}, Date: {sleep[1]}, Quality: {sleep[2]}, Duration: {sleep[3]} hours")
        else:
            print(f"No sleep entries found from {date} onwards.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_sleep_by_duration(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    while True:
        try:
            min_duration = float(input("Enter the minimum sleep duration (in hours): ").strip())
            if min_duration <= 0:
                raise ValueError("Sleep duration must be greater than 0.")
            break
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please try again.")

    try:
        query = "SELECT * FROM sleep WHERE duration >= %s and userId = %s ORDER BY duration ASC"
        cursor.execute(query, (min_duration,user_id))
        sleep_entries = cursor.fetchall()

        if sleep_entries:
            print(f"\nSleep entries with at least {min_duration} hours (sorted by duration):")
            for sleep in sleep_entries:
                print(f"ID: {sleep[0]}, Date: {sleep[1]}, Quality: {sleep[2]}, Duration: {sleep[3]} hours")
        else:
            print(f"No sleep entries found with at least {min_duration} hours.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_sleep_by_quality(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return

    cursor = mydb.cursor()

    sleep_quality = input("Enter the sleep quality to filter by (e.g., 'Good', 'Average', 'Poor'): ").strip()

    try:
        query = "SELECT * FROM sleep WHERE quality = %s and userId = %s ORDER BY sleepDate ASC"
        cursor.execute(query, (sleep_quality,user_id))
        sleep_entries = cursor.fetchall()

        if sleep_entries:
            print(f"\nSleep entries with quality '{sleep_quality}' (sorted by date):")
            for sleep in sleep_entries:
                print(f"ID: {sleep[0]}, Date: {sleep[1]}, Quality: {sleep[2]}, Duration: {sleep[3]} hours")
        else:
            print(f"No sleep entries found with quality '{sleep_quality}'.")

    except Error as e:
        print("Error during database operation:", e)

    finally:
        mydb.close()

def display_all_sleeps(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    query = "SELECT * FROM sleep where userid = %s ORDER BY sleepDate ASC"
    cursor.execute(query,(user_id,))
    sleep_entries = cursor.fetchall()
    if sleep_entries:
        print(f"\nAll sleep entries:")
        for sleep in sleep_entries:
            print(f"ID: {sleep[0]}, Date: {sleep[1]}, Quality: {sleep[2]}, Duration: {sleep[3]} hours")
    else:
        print(f"No sleep entries found.")
    mydb.close()

def display_sleep(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    choice = int(input("How do you want to see the sleep entries? \n"
                       "1. By ID \n"
                       "2. By date \n"
                       "3. By duration \n"
                       "4. By quality \n"
                       "5. Show all sleep entries \n"
                       "Enter your choice: "))
    while choice not in [1, 2, 3, 4, 5]:
        print("Invalid input. Please try again.")
        choice = int(input("Enter the choice number: "))
    if choice == 1:
        display_sleep_by_id(user_id)
    elif choice == 2:
        display_sleep_by_date(user_id)
    elif choice == 3:
        display_sleep_by_duration(user_id)
    elif choice == 4:
        display_sleep_by_quality(user_id)
    elif choice == 5:
        display_all_sleeps(user_id)

def delete_sleep(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()
    try:
        sleepId = int(input("Enter the Id of the sleep you would like to delete: "))
        if sleepId <= 0:
            raise ValueError("Invalid input. Please try again.")
        query_check = "Select * FROM sleep WHERE userid = %s AND sleepId = %s;"
        cursor.execute(query_check, (user_id, sleepId))
        sleep = cursor.fetchone()
        if not sleep:
            print(f"No sleep entry with id {sleepId} found.")
            mydb.close()
            return

        sleepDate = sleep[3]
        sleepDate = reverse_convert_date(sleepDate)
        while True:
            confirm = input(f"Are you sure you want to delete the sleep {sleepId} from the {sleepDate} ? (y/n): ").lower().strip()
            if confirm in ["y", "n"]:
                break
            print("Invalid input. Please try again.")
        if confirm == "y":
            query = "DELETE FROM sleep WHERE userid = %s AND sleepId = %s;"
            cursor.execute(query, (user_id,sleepId))
            mydb.commit()
            print("Sleep entry deleted.")
        else:
            print("Operation aborted.")
            return
        mydb.close()
    except ValueError as ve:
        print(f"Invalid input: {ve}. Please try again.")
    except Error as e:
        print("Error during database operation:", e)

def manage_sleep(user_id):
    print("\nSleep Management")
    print("1. Create Sleep Record")
    print("2. Modify Sleep Record")
    print("3. Display Sleep Records")
    print("4. Delete Sleep Record")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        create_sleep(user_id)
    elif choice == 2:
        modify_sleep(user_id)
    elif choice == 3:
        display_sleep(user_id)
    elif choice == 4:
        delete_sleep(user_id)
    else:
        print("Invalid choice.")

def plot_sleeps(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()




def update_user_info(user_id):
    mydb = connect_to_db()
    if not mydb:
        print("Database connection failed. Operation aborted.")
        return
    cursor = mydb.cursor()

    print("\nUpdate User Information")
    new_first_name = input("New first name (leave empty to keep current): ")
    new_last_name = input("New last name (leave empty to keep current): ")
    new_email = input("New email (leave empty to keep current): ")
    new_weight = input("New weight in kg (leave empty to keep current): ")
    new_height = input("New height in cm (leave empty to keep current): ")

    updates = {}
    if new_first_name:
        updates["firstName"] = new_first_name
    if new_last_name:
        updates["lastName"] = new_last_name
    if new_email:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            print("Error: Invalid email format.")
        else:
            updates["email"] = new_email
    if new_weight:
        try:
            updates["weight"] = float(new_weight)
        except ValueError:
            print("Error: Invalid weight. Must be a number.")

    if new_height:
        try:
            updates["height"] = float(new_height) / 100  # Convert cm to meters
        except ValueError:
            print("Error: Invalid height. Must be a number.")
    if updates:
        update_query = "UPDATE user SET " + ", ".join(f"{key} = %s" for key in updates.keys()) + " WHERE userId = %s"
        values = list(updates.values()) + [user_id]

        try:
            cursor.execute(update_query, values)
            cursor.commit()
            print("Update successful!")
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
    else:
        print("No changes were made.")

    cursor.close()


#Weight prediction

def weight_prediction(user_id):
    try:
        mydb = connect_to_db()
        if not mydb:
            print("Database connection failed. Operation aborted.")
            return

        cursor = mydb.cursor()
        query = "SELECT weight FROM user WHERE userid = %s AND weight IS NOT NULL;"
        cursor.execute(query, (user_id,))
        weight = [w[0] for w in cursor.fetchall()]
        mydb.close()

        if not weight:
            print("No weight data available for this user.")
            return

        df = pd.DataFrame(weight, columns=["weight"])
        df["weeks"] = np.arange(1, len(df) + 1)

        # Training
        model = LinearRegression()
        model.fit(df["weeks"].values.reshape(-1,1), df["weight"].values)

        # Predictions for the next 10 weeks
        ten_next_weeks = np.arange(len(df) + 1, len(df) + 11).reshape(-1, 1)
        prediction = model.predict(ten_next_weeks)

        prediction_df = pd.DataFrame({
            "Weeks": range(len(df) + 1, len(df) + 11),
            "Predicted weight (in kg)": prediction
        })

        print(prediction_df)

    except Exception as e:
        print(f"An error occurred: {e}")









