from random import randint
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

#trying to create a table
try:
    cur.execute('''CREATE TABLE accounts
    (id INTEGER PRIMARY KEY, number VARCHAR, pin VARCHAR, balance INTEGER DEFAULT 0);''')
    conn.commit()
    conn.close()
except:
    pass

def add_account():
    pin = int("".join(generate_pin()))
    card_number = int("".join(generate_card_number()))
    print("Your card has been created")
    print("Your card number:")
    print(card_number)
    print()
    print("Your card PIN:")
    print(pin)
    print()
    cur.execute('''INSERT INTO accounts (number, pin)
    VALUES(?,?)
    ''', [pin, card_number])
    conn.commit()
    conn.close()

class Account:
    def __init__(self, number, pin):
        self.number = number
        self.pin = pin


def control_number(tab):
    suma = 8
    for i in range(6, 15):
        if i % 2 == 0:
            suma += int(tab[i]) * 2
            if int(tab[i]) * 2 > 9:
                suma -= 9
        else:
            suma += int(tab[i])

    if suma % 10:
        return str(10 - suma % 10)
    else:
        return '0'


def generate_card_number():
    card_num = ['4', '0', '0', '0', '0', '0']
    for i in range(6, 15):
        card_num.append(str(randint(0, 9)))
    control_number(card_num)
    return card_num


def generate_pin():
    pin_num = []
    for i in range(4):
        pin_num.append(str(randint(0, 9)))
    return pin_num


def print_number(tab):
    for number in tab:
        print(number, end="")


def user_menu():
    while True:
        print("1. Balance")
        print("2. Log out")
        print("0. Exit")
        choice = int(input())
        if choice == 1:
            print("Balance: 0")
        elif choice == 2:
            print("You have successfully logged out!")
            break
        elif choice == 0:
            print("Bye!")
            exit()


data = []
# main menu

while True:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    choose = int(input())
    if choose == 1:
        add_account()
    elif choose == 2:
        print("Enter your card number:")
        card_number = [int(n) for n in list(input())]
        print("Enter your PIN:")
        pin_number = [int(n) for n in list(input())]
        for i in range(0, len(data)):
            if card_number == data[i].number and data[i].pin == pin_number:
                print("You have successfully logged in!")
                print()
                user_menu()
            else:
                print("Wrong card number or PIN!")
    elif choose == 0:
        print("Bye!")
        exit()
