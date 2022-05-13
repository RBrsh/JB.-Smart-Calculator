import re
import operator


class SmartCalculator:
    def __init__(self):
        self.__operations = {'command':
                                 [r'^/\w+', self.__execute_command],
                             'declaration':
                                 ['.*=.*', self.__process_declaration],
                             'retrievement':
                                 ['^[A-z]+$', self.__retrieve_variable],
                             'calculation':
                                 [r'^ *[-]*[A-Za-z()\d]+[ +-]*',
                                  self.__calculate],
                             }
        self.__valid_declare_patters = ('^ *([A-z]+) *=',
                                        r'^[^=]+= *((-?\d+)|([A-Za-z]+)) *$',)
        self.__declaration_errors = ('Invalid identifier',
                                     'Invalid assignment',)
        self.__variable_errors = ('Unknown variable',)
        self.__help_message = '''The program calculates simple arithmetic 
        expressions, understands several commands and can use variables in
        calculations.'''
        self.__bye_message = 'Bye'
        self.__expression_messages = ('Invalid expression',)
        self.__command_messages = ('Unknown command',)
        self.__operators = {'-': [1, operator.sub],
                            '+': [1, operator.add],
                            '*': [2, operator.mul],
                            '/': [2, operator.truediv],
                            '^': [3, operator.pow],
                            }
        self.__okfr = ''.join(self.__operators.keys())  # Operators keys for RE
        self.user_variables = {}

    def process_input(self, user_input: str) -> None:
        """
        Processes user input and takes action depending on the input: executes
        commands, stores variable, calculates expressions. Results are printed
        to stdout.
        :param user_input:
        :return: None
        """
        for operation, pattern in self.__operations.items():
            if re.match(pattern[0], user_input):
                self.__operations[operation][1](user_input)
                return

    def __execute_command(self, command):
        command = command[1:]  # Get rid of / at the beginning

        if command == 'exit':
            print(self.__bye_message)
            exit()
        elif command == 'help':
            print(self.__help_message)
        else:
            print(self.__command_messages[0])

    def __process_declaration(self, declaration: str) -> None:
        res = []
        for i, pattern in enumerate(self.__valid_declare_patters):
            m = re.search(pattern, declaration)
            if not m:
                print(self.__declaration_errors[i])
                return

            if i > 0:
                if m.group(1) in self.user_variables.keys():
                    res.append(self.user_variables[m.group(1)])
                elif re.match(r'\d+', m.group(1)):
                    res.append(m.group(1))
                else:
                    print(self.__declaration_errors[i])
                    return
            else:
                res.append(m.group(1))

        if res and len(res) == 2:
            self.user_variables.update({res[0]: res[1]})

    def __retrieve_variable(self, name: str) -> None:
        variable_value = self.user_variables.setdefault(name.strip())
        if variable_value is not None:
            print(variable_value)
        else:
            print(self.__variable_errors[0])

    def __calculate(self, expression: str) -> None:
        if self.__is_valid_expression(expression):
            result = self.__calculate_postfix(
                self.__convert_to_postfix(expression)
            )
            if result is not None:
                print(result)
        else:
            print(self.__expression_messages[0])
        return

    def __calculate_postfix(self, postfix: list):
        result = []

        for i in postfix:
            if re.match(r'\d+$', i):
                result.append(int(i))
            elif re.match('[A-Za-z]+$', i):
                try:
                    result.append(int(self.user_variables[i]))
                except KeyError:
                    print(self.__variable_errors[0])
                    return
            elif i in self.__operators:
                b, a = result.pop(), result.pop()
                result.append(self.__operators[i][1](a, b))

        if len(result) == 1:
            # Convert to int to get rif of decimal part if it's zero.
            int_result = int(result[0])
            return int_result if result[0] == int_result else result[0]

    def __convert_to_postfix(self, infix: str) -> list:
        stack = []
        postfix = []

        infix = infix.replace(' ', '')
        infix = re.sub(r'(\+)\+*', r'\1', infix)

        for i in re.finditer('-{2,}', infix):
            if (i.end() - i.start()) % 2 == 0:
                infix = infix[:i.start()] + '+' + infix[i.end():]
            else:
                infix = infix[:i.start()] + infix[i.end() - 1:]

        for i in re.findall(rf'[{self.__okfr}()]|\d+|[A-z]+', infix):
            if re.match(r'\d+|[A-Za-z]+', i):
                postfix.append(i)
                continue
            elif i in self.__operators:
                if not stack or stack[-1] == '(':
                    stack.append(i)
                    continue

                if self.__operators[i][0] > self.__operators[stack[-1]][0]:
                    stack.append(i)
                    continue
                else:
                    while stack:
                        postfix.append(stack.pop())
                        if not stack or\
                                self.__operators[i][0] <\
                                self.__operators[stack[-1]][0] or\
                                stack[-1] == '(':
                            stack.append(i)
                            break
            elif i == '(':
                stack.append(i)
            elif i == ')':
                while stack:
                    if stack[-1] == '(':
                        stack.pop()
                        break
                    postfix.append(stack.pop())

        while stack:
            postfix.append(stack.pop())

        return postfix

    @staticmethod
    def __is_valid_expression(expression):
        if len(expression) > 0 and expression[1] != ')' and \
                expression.count('(') == expression.count(')') and \
                not re.search('[*/]{2,}', expression):
            return True
        return False


def main():
    calc = SmartCalculator()
    while True:
        ui = input()
        calc.process_input(ui)


if __name__ == '__main__':
    main()
