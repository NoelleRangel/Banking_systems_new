import random
import sqlite3
conn = sqlite3.connect("example.db")  # This creates or opens the file "example.db" as a database
c = conn.cursor()


#c.execute("DROP TABLE IF EXISTS user") # Delete all records from the user table (previous runs)


# Create table
c.execute("""
CREATE TABLE IF NOT EXISTS user (
    username TEXT NOT NULL,
    acc_id INTEGER NOT NULL,
    password INTEGER NOT NULL,
    balance INTEGER NOT NULL)
""")

# Create table
c.execute("""
CREATE TABLE IF NOT EXISTS administrator (
    username TEXT NOT NULL,
    password INTEGER NOT NULL)
""")

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
    global account_type
    global choice
    print("Welcome to the Bank of America")
    choice = int(input("Enter 1 to create an account, 2 to log in: "))
    account_type = int(input("Enter 1 for user account, 2 for administrator: "))
    username = input("Enter your username: ")
    password = int(input("Enter your password (ex: 8746): "))

    if choice == 1:
        if account_type == 2:
            c.execute("INSERT INTO administrator VALUES (?, ?)", (username, password))

        elif account_type == 1:
            global new_account_num
            new_account_num = random.randint(0000000, 9999999)
            balance = int(input("Enter your balance: "))
            c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (username, new_account_num, password, balance))
        print("Sign Up Successful")

    elif choice == 2:
        if account_type == 1:
            c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
            result = c.fetchone()  # Fetch the first result
            if result:                    # Check if a result was found
                print("Login Successful")
            elif result is None:
                print("Invalid credentials")
                sign_up()
            global old_account_num
            old_account_num = result[1]    # Get the account number from the result
            
        elif account_type == 2:
            c.execute("SELECT * FROM administrator WHERE username = ? AND password = ?", (username, password))
            result = c.fetchone()  # Fetch the first result
            if result:                    # Check if a result was found
                print("Login Successful")
            elif result is None:
                print("Invalid credentials")
                sign_up()




def user_options():
    if account_type == 2:
        while True:
            print("Users: ")
            print_users()
            account = input("What is the account number of the user you want to inspect? ")
            c.execute("SELECT * FROM user WHERE acc_id = ?", (account,))
            user_acc = c.fetchone()  # Fetch the first result
            if user_acc:
                account_num = user_acc[1]
                print(f"{user_acc[0]} selected")
                print("0. Logout user only")
                break
            elif user_acc is None:
                print("No such user exists")

    print("1. Full logout")
    print("2. View user info")
    print("3. Close user account")

    if account_type == 1:
        if choice == 1:
            account_num = new_account_num
        elif choice == 2:
            account_num = old_account_num
        c.execute("SELECT * FROM user WHERE acc_id = ?", (account_num,))
        user_acc = c.fetchone()  # Fetch the first result
        print("4. Deposit money")
        print("5. Withdraw money")
        print("6. Change user info")
        
    option = int(input("Enter your option: "))

    if option == 1:
        print("Logging out...")
        conn.commit()

    elif option == 2:
        print("User details:")
        print(f"Username: {user_acc[0]}, Account num: {user_acc[1]}, Password: {user_acc[2]}, Balance: {user_acc[3]}")

    elif option == 3:
        c.execute("DELETE FROM user WHERE acc_id = ?", (account_num,))
        print("Account closed successfully")

    elif option == 4:
        ammount = int(input("Enter the amount you want to deposit: "))
        c.execute("UPDATE user SET balance = ? WHERE acc_id = ?", (user_acc[3] + ammount, account_num,))
        print(f"{ammount} deposited sucessfully")

    elif option == 5:
        ammount = int(input("Enter the amount you want to withdraw: "))
        c.execute("UPDATE user SET balance = ? WHERE acc_id = ?", (user_acc[3] - ammount, account_num,))
        print(f"{ammount} withdrawn sucessfully")        #realistic debt system.

    elif option == 6:
        change_item = input("Which value would you like to change? (username or password): ")
        change_value = input("What would you like to change it to? ")
        c.execute(f"UPDATE user SET {change_item} = ? WHERE acc_id = ?", (change_value, account_num,))
        print("User info changed successfully")

    conn.commit()
    if account_type == 1 or option == 0:
        user_options()    #recursive function to keep the program running
    if option == 1 or option == 3:
        sign_up()        #bring the user back to the sign up screen




# Call the function after signing up a user or wherever appropriate
sign_up()
conn.commit()
user_options()