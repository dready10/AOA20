def recite(starting_ages, until_epoch):
    epoch = len(starting_ages.keys()) + 1
    turn = 0
    while epoch < until_epoch:
        if turn in starting_ages.keys():
            new_turn = epoch - starting_ages[turn]
            starting_ages[turn] = epoch
            turn = new_turn
        else:
            starting_ages[turn] = epoch
            turn = 0
        epoch += 1
    print(str(epoch) + ': ' + str(turn))

# starting state
ages = {14: 1, 8: 2, 16: 3, 0: 4, 1: 5, 17: 6}

# part 1 and 2
recite(ages, 2020)

# reset
ages = {14: 1, 8: 2, 16: 3, 0: 4, 1: 5, 17: 6}
recite(ages, 30000000)