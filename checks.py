from random import randint

def generate_pin():
    pin_num = []
    for i in range (3):
        pin_num.append(randint(0,9))
    return pin_num

data = generate_pin()

print(data)