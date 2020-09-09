import random
import sqlite3

conn = sqlite3.connect('card.s3db')
c = conn.cursor()

c.execute("""
            CREATE TABLE IF NOT EXISTS card(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number    TEXT UNIQUE,
                pin       TEXT,
                balance   INTERGER DEFAULT 0
            );
        """)


card_info = {}


def login():
    print("You have successfully logged in!")
    while True:
        operation = input("""
1. Balance
2. Log out
0. Exit
""")
        if operation == "1":
            print("Balance: 0")
        elif operation == "2":
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
    params = (number, random_pin)
    c.execute("INSERT INTO card (number, pin) VALUES (?, ?)", params)


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
                login()
            else:
                print("Wrong card number or PIN!")
        else:
            print("Wrong card number or PIN!")

    elif action == "0":
        print("Bye!")
        break

conn.commit()
c.close()
