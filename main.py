"""
This is a simple bank program that allows users to create accounts, close them, deposit money, withdraw money, and change their info. It also allows administrators to inspect user accounts, log out users, and close user accounts.
I used sqlite3 to create a database and store the user and administrator info and Python to create the program.
I chose to use a command-line interface for simplicity, you may find it in a 'console' tab in your IDE.
"""


import random
import sqlite3
conn = sqlite3.connect("example.db")  # This creates or opens the file "example.db" as a database
c = conn.cursor()

#This code erase the table values everytime the program is run.
c.execute("DROP TABLE IF EXISTS user")
c.execute("DROP TABLE IF EXISTS administrator")


#All users need a username, account number, password, and balance.
c.execute("""
CREATE TABLE IF NOT EXISTS user (
    username TEXT NOT NULL,
    acc_id INTEGER NOT NULL,
    password INTEGER NOT NULL,
    balance INTEGER NOT NULL)
""")

#Administrators do not need a balance or account number.
c.execute("""
CREATE TABLE IF NOT EXISTS administrator (
    username TEXT NOT NULL,
    password INTEGER NOT NULL)
""")





# Some users and an administrator have been provided. You can use them or create your own.
# These are printed at the start of the program to show the values for later testing.

c.execute("INSERT INTO user VALUES"
"('Nala', 1234567, 8746, 1000453),"
"('Candy', 7654321, 6748, 2453),"
"('Arielle', 3457995, 2432, 5645),"
"('Jake', 2345678, 5678, 30034),"
"('Devan', 2345678, 5678, 30034)")

c.execute("INSERT INTO administrator VALUES"
"('Admin', 5768),"
"('Boss', 9873)")


# Save the changes
conn.commit()






def print_users():
    c.execute("SELECT * FROM user")  # Fetch all records from the user table
    rows = c.fetchall()               # Get all rows returned by the query
    for row in rows:                  # Iterate through each record
        print(row)                    # Print the record

def print_admins():
    c.execute("SELECT * FROM administrator")  # Fetch all records from the administrator table
    rows = c.fetchall()               # Get all rows returned by the query
    for row in rows:                  # Iterate through each record
        print(row)                    # Print the record





def sign_up():
    print_users()        # Print all users from the table
    print_admins()        # Print all administrators from the table
    global account_type    #Globalization allows the program to remember variables.
    global choice
    print("Welcome to the Bank of America")
    choice = int(input("Enter 1 to create an account, 2 to log in: "))
    account_type = int(input("Enter 1 for user account, 2 for administrator: "))
    username = input("Enter your username: ")
    password = int(input("Enter your password (ex: 8746): "))

    
    #If a new user signs up.
    if choice == 1 and account_type == 1:
        global new_account_num
        new_account_num = random.randint(0000000, 9999999)    #Generates a random, permanent, account number.
        balance = int(input("Enter your balance: "))
        c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (username, new_account_num, password, balance))
        print("Sign Up Successful")

    
    #If a new administrator signs up.
    if choice == 1 and account_type == 2:
        c.execute("INSERT INTO administrator VALUES (?, ?)", (username, password))

    
    #If an existing user logs in.
    if choice == 2 and account_type == 1:
        c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()  # Fetch the first result
        if result:                    # Checks if the account exists.
            print("Login Successful")
        elif result is None:
            print("Invalid credentials")
            sign_up()                   #Repeats the sign up process until the administrator enters valid credentials.
        global old_account_num
        old_account_num = result[1]    # Get the account number from the result

        
    #If an existing administrator logs in.
    if choice == 2 and account_type == 2:
        c.execute("SELECT * FROM administrator WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()
        if result:
            print("Login Successful")
        elif result is None:
            print("Invalid credentials")
            sign_up()                  #Repeats the sign up process until the administrator enters valid credentials.




    

def user_options():
    #This if statement is to allow the admin to select a user to inspect.
    if account_type == 2:
        #This while loop is to prevent the admin from selecting a user that does not exist.
        while True:
            print("Users: ")
            print_users()
            account = input("What is the account number of the user you want to inspect? ")
            c.execute("SELECT * FROM user WHERE acc_id = ?", (account,))
            user_acc = c.fetchone()  # Fetch the first result
            if user_acc:
                account_num = user_acc[1]
                print(f"{user_acc[0]} selected")
                print("0. Logout user only")              #Only allow the admin to view user logout.
                break
            elif user_acc is None:
                print("No such user exists, try again")

    #Everyone can see these options.
    print("1. Full logout")
    print("2. View user info")
    print("3. Close user account")

    #This if statement extracts the account number from the user that logged in.
    if account_type == 1:
        if choice == 1:
            account_num = new_account_num
        elif choice == 2:
            account_num = old_account_num
        c.execute("SELECT * FROM user WHERE acc_id = ?", (account_num,))
        user_acc = c.fetchone()  # Fetch the first result
        #Only allow the user to deposit, withdraw, and change their info.
        print("4. Deposit money")
        print("5. Withdraw money")
        print("6. Change user info")
    option = int(input("Enter your option: "))

    #Both users and admins will be logged out.
    if option == 1:
        print("Logging out...")
        conn.commit()

    #Users and admins can view user info.
    elif option == 2:
        print("User details:")
        print(f"Username: {user_acc[0]}, Account num: {user_acc[1]}, Password: {user_acc[2]}, Balance: {user_acc[3]}")

    #Users and admins can close user accounts.
    elif option == 3:
        c.execute("DELETE FROM user WHERE acc_id = ?", (account_num,))
        print("Account closed successfully")

    #Only users can interact with their balance
    elif option == 4:
        ammount = int(input("Enter the amount you want to deposit: "))
        c.execute("UPDATE user SET balance = ? WHERE acc_id = ?", (user_acc[3] + ammount, account_num,))
        print(f"{ammount} deposited sucessfully")

    elif option == 5:
        ammount = int(input("Enter the amount you want to withdraw: "))
        if ammount <= user_acc[3]:
            c.execute("UPDATE user SET balance = ? WHERE acc_id = ?", (user_acc[3] - ammount, account_num,))
            print(f"{ammount} withdrawn sucessfully")
        else:       #Prevents the user from going into debt.
            print("Insufficient funds")

    #Only users can change their info. Their account number stays consistent.
    elif option == 6:
        change_item = input("Which value would you like to change? (username or password): ")
        change_value = input("What would you like to change it to? ")
        c.execute(f"UPDATE user SET {change_item} = ? WHERE acc_id = ?", (change_value, account_num,))
        print("User info changed successfully")

    conn.commit()
    #If anyone logs out or a user closes their account, they will be brought back to the sign up screen.
    if option == 1 or (option == 3 and account_type == 1):
        sign_up()
    #If any user or admin selects option 0 or 3, they will be brought back to the options screen.
    if account_type == 1 or option == 0 or option == 3 or (option == 2 and account_type == 2):
        user_options()    #recursive function to keep the program running



        

#The order these pre-baked functions are called.
sign_up()
conn.commit()
user_options()