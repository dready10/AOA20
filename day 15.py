def recite(recited_number_ages, final_turn):
    turn = len(recited_number_ages.keys()) + 1
    recited_number = 0
    while turn < final_turn:
        if recited_number in recited_number_ages.keys():
            next_number_to_recite = turn - recited_number_ages[recited_number]
            recited_number_ages[recited_number] = turn
            recited_number = next_number_to_recite
        else:
            recited_number_ages[recited_number] = turn
            recited_number = 0
        turn += 1
    print(str(turn) + ': ' + str(recited_number))

# starting state
recited_number_ages = {14: 1, 8: 2, 16: 3, 0: 4, 1: 5, 17: 6}

# part 1
recite(recited_number_ages, 2020)

# reset and part 2
recited_number_ages = {14: 1, 8: 2, 16: 3, 0: 4, 1: 5, 17: 6}
recite(recited_number_ages, 30000000)