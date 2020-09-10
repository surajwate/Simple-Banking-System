import random
import sqlite3

conn = sqlite3.connect('card.s3db')  # Create database ("card.s3db") connection
c = conn.cursor()  # create cursor object 'c'

# Create the table "card" if it does not exist in database
c.execute("""
            CREATE TABLE IF NOT EXISTS card(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number    TEXT,
                pin       TEXT,
                balance   INTEGER
            );
        """)
#  Remove everthing (old data) from table "card". You can delete this line if you want to maintain the database.
c.execute("DELETE FROM card")

card_info = {}

def get_balance(card):
    c.execute(f"SELECT balance FROM card WHERE number = {card}")
    return c.fetchone()[0]

def do_transfer(card):
    account = input("Enter card number:")  # get the card number to which the amount is to be transferred
    c.execute("SELECT number FROM card")  # Select the number column from table "card" of the database
    a_list = c.fetchall()  # Fetch all the selected numbers from number column in form of tuple in a list
    account_list = [i[0] for i in a_list]  # convert the list of tuple into list of integer (account numbers)
    if luhn_algo(account[:-1]) != account[-1]:  # check the validity of account number by using luhn algorithm
        print("Probably you made a mistake in the card number. Please try again!")
    elif account not in account_list:
        print("Such a card does not exist.")
    else:
        amount = int(input("Enter how much money you want to transfer:"))
        balance = get_balance(card)
        if balance < amount:
            print("Not enough money!")
        else:
            balance = get_balance(card)
            c.execute(f"""
                            UPDATE card
                            SET balance = {balance - amount}
                            WHERE number = {card}
            """)
            conn.commit()
            balance = get_balance(account)
            c.execute(f"""
                            UPDATE card
                            SET balance = {balance + amount}
                            WHERE number = {account}
            """)
            conn.commit()
            print("Success!")

def login(card):
    print("You have successfully logged in!")
    while True:
        operation = input("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")
        if operation == "1":
            balance = get_balance(card)
            print(f"Balance: {balance}")
        elif operation == '2':
            amount = int(input("Enter income:"))
            balance = get_balance(card)
            c.execute(f"""
                            UPDATE card
                            SET balance = {balance + amount}
                            WHERE number = {card}
            """)
            conn.commit()
            print("Income was added!")
        elif operation == '3':
            do_transfer(card)
        elif operation == '4':
            pass
        elif operation == "5":
            print("You have successfully logged out!")
            return None
        elif operation == '0':
            exit()


# Luhn Algorithms
def luhn_algo(ctrl_data):
    count, sums = 0, 0
    for i in ctrl_data:
        i = int(i)
        if count % 2 == 0:
            i = i * 2
        if i > 9:
            i = i - 9
        sums = sums + i
        count += 1
    ctrl_number = 10 - sums % 10
    return str(ctrl_number)


# Create new back account number for credit_card()
def bank_account_number():
    account_number = 100000001
    while True:
        if ('400000' + str(account_number) + luhn_algo('400000' + str(account_number))) in card_info:
            account_number += 1
        else:
            return str(account_number)


def create_card():
    number = '400000' + bank_account_number() + luhn_algo('400000' + str(bank_account_number()))
    random_pin = random.randrange(1000, 9999)
    card_info[number] = random_pin
    print("""
Your card has been created
Your card number:
{}
Your card PIN:
{}""".format(number, random_pin))
    balance = 0
    params = (number, random_pin, balance)
    c.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", params)  # Update the table "card" in database
    conn.commit()  # commit the changes in database to avoid the locking of database


while True:
    action = input("""
1. Create an account
2. Log into account
0. Exit
""")

    if action == "1":
        create_card()

    elif action == "2":
        card_number = input("\nEnter your card number:\n")
        pin = int(input("Enter your PIN:\n"))
        if card_number in card_info:
            if pin == card_info[card_number]:
                login(card_number)
            else:
                print("Wrong card number or PIN!")
        else:
            print("Wrong card number or PIN!")

    elif action == "0":
        print("Bye!")
        break

conn.commit()
c.close()
