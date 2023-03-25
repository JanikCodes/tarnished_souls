

def create_bars(value, max):
    perc = (float(value) / float(max)) * 100
    str = ""
    emp = ""
    first_digit = 0

    if perc >= 10:
        if perc == 100:
            first_digit = 10
        else:
            first_digit = int(perc // 10)

    for i in range(first_digit):
        str += ":blue_square:"
    for y in range(10 - first_digit):
        emp += ":black_large_square:"

    str += emp
    return str

def create_invisible_spaces(amount):
    white = ""
    for x in range(amount):
        white += "\u200E "
    return white