def compute(operand1, operator, operand2):
    if operator == '*':
        return int(operand1) * int(operand2)
    if operator == '+':
        return int(operand1) + int(operand2)
    return 0


def evaluate(expression, low_precedence_operators):
    # format the expression for tokenizing convenience
    expression = '(' + expression + ')'
    expression = expression.replace('(', '( ')
    expression = expression.replace(')', ' )')

    # here are our data structures
    tokens = expression.split(' ')
    operators = []
    operands = []

    # i actually had to write something like this back in uni, so
    # i already knew the answer. basically, in evaluating expressions
    # left-to-right, push stuff onto a stack as you encounter it. when you
    # encounter something that makes you evaluate an expression (a ')' or maybe
    # an int), both stacks until you finish evaluating the sub expression
    # rinse and repeat
    for token in tokens:
        if token == '(': # sub expression starts. 
            operators.append('(')
        elif token == ')': # sub expression has ended, need to complete evaluation of it.

            # to evaluate, pop operands and operators off their stacks and evaluate them
            while operators[-1] not in '(':
                operands.append(compute(operands.pop(), operators.pop(), operands.pop()))

            operators.pop() # get rid of the open paren

            # now that the sub expression is evaluated, we need to 
            # 'go backward' in the expression to finish evaluating the
            # pre-subexpression operators.
            # eg, in 2 * 3 + (5 * 1) * 3, we need to go backward after we evaluate 5 * 1
            # and evaluate the '+' before we evaluate any *. in the case of where
            # * and + are equal precedence, that means that * will already be evaluated
            # and we'll have 6 + 5 to evaluate before we get to * 3.
            # in the case of + having higher precedence, 2 * 3 will not have been evaluated
            # and we'll need to evaluate 3 + 5 before going to 8 * 3    
            while len(operators) > 0 and operators[-1] not in low_precedence_operators:
                operands.append(compute(operands.pop(), operators.pop(), operands.pop()))
        elif token in '+*':
            operators.append(token)
        else:
            # consider 2 * 3 + (5 * 1) again. 
            # in the case where + and * are equal precedence, we'd pop 2 and 3,
            # evaluate it with *, push 6 onto the stack, push + on, 
            # evaluate the subexpression then go back to evaluate 6 + 5.

            # in the case where + is higher precedence than *, for 2 * 3 + (5 * 1)
            # we want to NOT evaluate 2 * 3 until later. so if the top of the
            # operator stack is a * (eg, token == 3), just push the 3 token right on.
            # then, we get to the plus, evaluate the subexpression (5*1) and get to
            # 2 * 3 + 6. because after a subexpression we go backward to evaluate
            # any plusses, we'd get 2 * 9 for 18.
            if operators[-1] in low_precedence_operators:
                operands.append(token)
                continue
            operator = operators.pop()
            operand1 = operands.pop()
            operands.append(compute(operand1, operator, token))
    return operands[0]


with open('18input1.txt') as f:
    expressions = [x for x in f.read().split('\n')]
    total = 0

    # part 1
    for expression in expressions:
        total += evaluate(expression, '(')
    print(total)

    # part 2
    total = 0
    for expression in expressions:
        total += evaluate(expression, '(*')
    print(total)