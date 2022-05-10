import string
import re


class SmartCalculator:
    operation_types = {'command': r'^/\w+',
                       'declaration': '.*=.*',
                       'retrievement': '^[A-z]+$',
                       'calculation': r'^ *[-]*[A-z\d]+[ +-]*',
                       }
    valid_declaration = ('^ *([A-z]+) *=',
                         r'^[^=]+= *((-?\d+)|([A-z]+)) *$',
                         )
    declaration_errors = ('Invalid identifier', 'Invalid assignment')
    variable_errors = ('Unknown variable',)
    help_message = 'The program calculates the sum and difference of numbers.'
    bye_message = 'Bye'

    def __init__(self):
        self.handlers = {'command': self.__execute_command,
                         'declaration': self.__process_declaration,
                         'retrievement': self.__retrieve_variable,
                         'calculation': self.__calculate,
                         }
        self.variables = {}

    def process_input(self, user_input):
        for operation, pattern in self.operation_types.items():
            #print(f'{operation}: {pattern}, {user_input}')
            if re.match(pattern, user_input):
                #print('ddd')
                res = self.handlers[operation](user_input)
                return

    def __execute_command(self, command):
        command = command[1:]  # Get rid of / at the beginning

        if command == 'exit':
            print(self.bye_message)
            exit()
        elif command == 'help':
            print(self.help_message)
        else:
            print('Unknown command')

    def __process_declaration(self, declaration):
        res = []
        for i, pattern in enumerate(self.valid_declaration):
           # print(i, pattern, declaration)
            m = re.search(pattern, declaration)
            if not m:
                print(self.declaration_errors[i])
                return
            #print(m.groups())

            if i > 0:
                if m.group(1) in self.variables.keys():
                    res.append(self.variables[m.group(1)])
                elif re.match(r'\d+', m.group(1)):
                    res.append(m.group(1))
                else:
                    print(self.declaration_errors[i])
                    return
                   #print(f'Here: {self.variables[m.group(1)]}. {m.group(1)}')
            else:
                res.append(m.group(1))

        if res and len(res) == 2:
            self.variables.update({res[0]: res[1]})

    def __retrieve_variable(self, name):
        variable_value = self.variables.setdefault(name.strip())
        if variable_value is not None:
            print(variable_value)
        else:
            print(self.variable_errors[0])

    def __calculate(self, expression):
        el = expression.split()
        calc_stack = []
        negative = False

        for i in el:
           # if not is_valid_expression(i):
            #    print('Invalid expression')
             #   break

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

            var_value = self.variables.setdefault(i)
            if var_value:
                i = var_value

            if len([_ for _ in i if _ in string.digits]) == len(i):
                i = int(i)
                if negative:
                    #  print('Nega')
                    i = -i
                    negative = False
                # print(i)
                calc_stack.append(i)
            else:
                if determine_sign(i) == '-':
                    negative = True
        # print(calc_stack)
        if calc_stack:
            print(sum(calc_stack))

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


# valid_commands = ['/exit', '/help']

calc = SmartCalculator()

while True:
    ui = input()

    if ui == '':
        continue

    calc.process_input(ui)

    '''
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
        '''

