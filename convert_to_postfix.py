import re


def convert_to_postfix(infix: str):
    stack = []
    postfix = []
    operators = {'+': 1, '-': 1, '*': 2, '/': 2}

    for i in infix.split():
        if re.match(r'\d+|[A-z]+', i):
            stack.append(i)
            continue
        elif re.match('[+-]+|[*/]', i):

            if re.match(r'\d+', stack[-1]):
                stack.append(i)
                continue

            if not stack or stack[-1] == '(':
                stack.append(i)
                continue

            if operators[i] > operators[stack[-1]]:
                stack.append(i)
                continue
            else:
                pass



def main():
    convert_to_postfix('2 * (3 + 4) + 1')


if __name__ == '__main__':
    main()
