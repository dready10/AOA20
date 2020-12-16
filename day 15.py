def recite(recited_number_ages, until_epoch):
    epoch = len(recited_number_ages.keys()) + 1
    recited_number = 0
    while epoch < until_epoch:
        if recited_number in recited_number_ages.keys():
            next_number_to_recite = epoch - recited_number_ages[recited_number]
            recited_number_ages[recited_number] = epoch
            recited_number = next_number_to_recite
        else:
            recited_number_ages[recited_number] = epoch
            recited_number = 0
        epoch += 1
    print(str(epoch) + ': ' + str(recited_number))

# starting state
recited_number_ages = {14: 1, 8: 2, 16: 3, 0: 4, 1: 5, 17: 6}

# part 1
recite(recited_number_ages, 2020)

# reset and part 2
recited_number_ages = {14: 1, 8: 2, 16: 3, 0: 4, 1: 5, 17: 6}
recite(recited_number_ages, 30000000)