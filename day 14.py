
# used for part 2
def generate_addresses(floating_address):
    num_xs = floating_address.count('X')

    # for each possible address, go through and switch
    # an X for a 0 or 1. counting up from 0 through 2 ** num_xs
    # will enumerate each possible 0/1 pattern for any number
    # of Xs
    for i in range(2 ** num_xs):
        X_values_for_i = bin(i)[2:].zfill(num_xs)
        address = ''
        used_Xs = 0

        # replace Xs with the enumerated 0/1 value
        for bit in floating_address:
            if bit == 'X':
                address += X_values_for_i[used_Xs]
                used_Xs += 1
            else:
                address += bit

        yield int(address, 2)
        i+=1

with open('14input1.txt') as f:
    # part 1
    memory = {}
    for line in f.read().split('\n'):
        line = line.split(' = ')
        if line[0] == 'mask':
            mask1 = int(line[1].replace('X', '1'), 2)
            mask0 = int(line[1].replace('X', '0'), 2)
            continue
        # apply the mask
        memory[line[0]] = (int(line[1]) | mask0) & mask1
    
    total = 0
    for address in memory.keys():
        total += memory[address]
    print(total)

    # part 2
    f.seek(0)
    memory = {}
    for line in f.read().split('\n'):
        line = line.split(' = ')
        if line[0] == 'mask':
            mask = line[1]
            bit_mask = mask.replace('X', '0')
            continue

        # apply the non-floating part of the mask
        address = bin(int(line[0][4:-1]) | int(bit_mask, 2))[2:].zfill(36)

        # apply the floating part of the mask
        floating_address = ['X' if bit[0] == 'X' else bit[1] for bit in zip(list(mask), list(address))]
        
        for address in generate_addresses(floating_address):
            memory[address] = int(line[1])

    total = 0
    for key in memory.keys():
        total += memory[key]
    print(total)