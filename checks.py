
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

card = 4000003972196502

print(check_luhn(str(card)))