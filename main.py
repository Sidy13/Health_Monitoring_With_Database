from functions import *



def main():
    print(
        "Welcome in the health monitoring system ! \nDo you have an account or would you like to create a new account?")
    choice = int(input("1. Create an account\n2. Create a new account\nEnter your choice: "))
    while choice not in [1, 2]:
        choice = int(input("1. Create an account\n2. Create a new account\n"))
    if choice == 1:
        is_logged_in, user_id = login()
    if choice == 2:
        create_user()
    while True:
        print("\nHealth Tracker Main Menu")
        print("1. Manage Meals")
        print("2. Manage Workouts")
        print("3. Manage Sleep")
        print("4. Manage Users")
        print("5. Exit")

        choice = int(input("Enter your choice: "))
        while choice not in [1, 2, 3, 4, 5]:
            choice = int(input("Enter your choice: "))
        if choice == 1:
            manage_meals(user_id)
        elif choice == 2:
            manage_workouts(user_id)
        elif choice == 3:
            manage_sleep(user_id)
        elif choice == 5:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


