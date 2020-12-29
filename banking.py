from random import randint
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# trying to create a table
try:
    cur.execute('''CREATE TABLE card
    (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);''')
    conn.commit()
    conn.close()
except:
    pass

def check_luhn(str):
    suma = 0
    for i in range(len(str)):
        if i % 2 == 0:
            suma += int(str[i]) * 2
            if int(str[i]) * 2 > 9:
                suma -= 9
        else:
            suma += int(str[i])

    if suma % 10:
        return False
    else:
        return True


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
    card_num.append(control_number(card_num))
    return card_num


def generate_pin():
    pin_num = []
    for i in range(4):
        pin_num.append(str(randint(0, 9)))
    return pin_num


def print_number(tab):
    for number in tab:
        print(number, end="")


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
    cur.execute('''INSERT INTO card (number, pin)
    VALUES(?,?)
    ''', [card_number, pin])
    conn.commit()


def log_in(card_given, pin_given):
    card_number = (card_given, )
    cur.execute('''SELECT pin FROM card
    WHERE number = ?
    ''', card_number)
    pin_number = cur.fetchone()
    #converts pin to int
    if pin_number == None:
        print("Wrong card number or PIN!")
    elif pin_given != int("".join(str(x) for x in pin_number)):
        print("Wrong card number or PIN!")
        print()
    else:
        print("You have successfully logged in!")
        user_menu(card_number)


def user_menu(card_number):
    while True:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        choice = int(input())
        if choice == 1:
            cur.execute("""SELECT balance FROM card
            WHERE number = ?
            """, card_number)
            balance = int("".join(str(x) for x in cur.fetchone()))
            print("Balance: {}".format(balance))
        elif choice == 2:
            cur.execute("""SELECT balance FROM card
            WHERE number = ?
            """, card_number)
            actual_balance = int("".join(str(x) for x in cur.fetchone()))
            print("Enter income:")
            actual_balance += int(input())
            card_number = int("".join(str(x) for x in card_number))
            cur.execute("""UPDATE card
            SET balance = ?
            WHERE number = ?
            """, [actual_balance, card_number])
            card_number = (card_number,)
            conn.commit()
            print("Income was added!")
        elif choice == 3:
            cur.execute("""SELECT balance FROM card
                                    WHERE number = ?
                                    """, card_number)
            actual_balance = int("".join(str(x) for x in cur.fetchone()))
            print("Transfer")
            print("Enter card number:")
            transfer_card = int(input())
            tupel = (transfer_card,)

            cur.execute("""SELECT balance FROM card
            WHERE number = ?
            """, tupel)
            if int("".join(str(x) for x in card_number) == transfer_card):
                print("You can't transfer money to the same account!")
            elif check_luhn(str(transfer_card)) == False:
                print("Probably you made a mistake in the card number. Please try again!")
            elif cur.fetchone() == None:
                print("Such a card does not exist.")
            else:
                print("Enter how much money you want to transfer:")
                to_transfer = int(input())
                if to_transfer > actual_balance:
                    print("Not enough money!")
                else:
                    cur.execute("""SELECT balance FROM card
                                WHERE number = ?
                                """, tupel)
                    target_balance = int("".join(str(x) for x in cur.fetchone()))
                    target_balance += to_transfer
                    cur.execute("""UPDATE card
                                SET balance = ?
                                WHERE number = ?
                                """, [target_balance, transfer_card])
                    conn.commit()
                    actual_balance -= to_transfer
                    card_number = int("".join(str(x) for x in card_number))
                    cur.execute("""UPDATE card
                                                SET balance = ?
                                                WHERE number = ?
                                                """, [actual_balance, card_number])
                    conn.commit()
                    card_number = (card_number,)
        elif choice == 4:
                cur.execute("""DELETE FROM card
            WHERE number = ?
            """, card_number)
                conn.commit()
                print("The account has been closed!")
        elif choice == 5:
            break
        elif choice == 0:
            print("Bye!")
            exit()

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
        card_number = int(input())
        print("Enter your PIN:")
        pin_number = int(input())
        log_in(card_number, pin_number)
    elif choose == 0:
        print("Bye!")
        conn.close()
        exit()
