import string
import re

def determine_sign(sign_string: str) -> str:
    sign = ''

    for s in sign_string:
        if not sign:
            sign = s
            continue

        if s == sign and s == '-':
            sign = '+'
            continue

        if s != sign and s == '-':
            sign = '-'
            continue

    #print(f'{sign_string}: {sign}')
    return sign


def is_valid_expression(string_to_check):
    if re.match('(^[+-]*\d+$)|([+-]+)', string_to_check):
        return True
    return False


def is_valid_command(string_to_check):
    if string_to_check in valid_commands:
        return True
    return False


valid_commands = ['/exit', '/help']


while True:
    ui = input()

    if ui == '':
        continue

    if ui[0] == '/' and not is_valid_command(ui):
        print('Unknown command')
        continue

    if ui == '/exit':
        print('Bye!')
        break
    elif ui == '':
        continue
    elif ui == '/help':
        print('The program calculates the sum and difference of numbers')
    else:
        ui = ui.split()
        calc_stack = []
        negative = False

        for i in ui:
            if not is_valid_expression(i):
                print('Invalid expression')
                break

            if i == '+':
                continue
            if i == '-':
                negative = True
                continue

            if i[0] == '+':
                i = i[1:]

            if i[0] == '-' and len(i) >= 2 and i[1] in string.digits:
                negative = True
                i = i[1:]

            if len([_ for _ in i if _ in string.digits]) == len(i):
                i = int(i)
                if negative:
                  #  print('Nega')
                    i = -i
                    negative = False
                #print(i)
                calc_stack.append(i)
            else:
                if determine_sign(i) == '-':
                    negative = True
        #print(calc_stack)
        if calc_stack:
            print(sum(calc_stack))

