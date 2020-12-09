def execute(instructions):
    ip = 0
    acc = 0
    while ip < len(instructions):
        if(instructions[ip][2] == 'y'):
            break
        instructions[ip][2] = 'y'
        
        if (instructions[ip][0] == 'acc'):
            acc += int(instructions[ip][1])
        
        if (instructions[ip][0] == 'jmp'):
            ip += int(instructions[ip][1]) - 1

        ip += 1

    return (acc, ip >= len(instructions))

with open('8input1.txt', 'r') as f:
    #[[instruction, operand, 'die?'],...]
    instructions = [(instruction + ' n').split(' ') for instruction in f.read().split('\n')]

    #part 1
    print(execute(instructions)[0])

    #part 2
    for i, instruction in enumerate(instructions):
        #reset "die" to "no" for all instructions
        instructions = [[ins[0], ins[1], 'n'] for ins in instructions]

        #individually swap a jmp and nop and test to see if the "error code" is true
        #if it is, that's the answer
        if instruction[0] == 'jmp':
            instructions[i][0] = 'nop'
            acc, success = execute(instructions)
            if success:
                print(acc)
                break
            instructions[i][0] = 'jmp'
        if instruction[0] == 'nop':
            instructions[i][0] = 'jmp'
            acc, success = execute(instructions)
            if(success):
                print(acc)
                break
            instructions[i][0] = 'nop'
