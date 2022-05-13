import operator
import re


def convert_to_postfix(infix: str) -> list:
    stack = []
    postfix = []
    operators = {'-': 1, '+': 1, '*': 2, '/': 2, '^': 3}
    ofr = ''.join(operators.keys())

    infix = infix.replace(' ', '')
    infix = re.sub(r'(\+)\+*', r'\1', infix)

    for i in re.finditer('-{2,}', infix):
        if (i.end() - i.start()) % 2 == 0:
            infix = infix[:i.start()] + '+' + infix[i.end():]
        else:
            infix = infix[:i.start()] + infix[i.end() - 1:]

    for i in re.findall(rf'[{ofr}()]|\d+|[A-z]+', infix):
        if re.match(r'\d+|[A-Za-z]+', i):
            postfix.append(i)
            continue
        elif i in operators:
            if not stack or stack[-1] == '(':
                stack.append(i)
                continue

            if operators[i] > operators[stack[-1]]:
                stack.append(i)
                continue
            else:
                while stack:
                    postfix.append(stack.pop())
                    if not stack or operators[i] < operators[stack[-1]] \
                            or stack[-1] == '(':
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


def calculate_postfix(postfix: list):
    print(postfix)
    result = []
    operators = {'-': operator.sub,
                 '+': operator.add,
                 '*': operator.mul,
                 '/': operator.truediv,
                 '^': operator.pow}

    for i in postfix:
        if re.match(r'\d+$', i):
            result.append(int(i))
        elif re.match('[A-Za-z]+$', i):
            pass
        elif i in operators:
            b, a = result.pop(), result.pop()
            result.append(operators[i](a, b))

    if len(result) == 1:
        return result[0]


def main():
    print(calculate_postfix(convert_to_postfix('2*2^3')))


if __name__ == '__main__':
    main()
