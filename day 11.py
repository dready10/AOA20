def tick(game):
    # need a copy to manipulate while keeping the reference state pure
    new_state = [list(row) for row in game]
    seat_count = 0

    # iterate through each tile and (for k / for i) then count
    # the number of occupied seats surrounding it
    for i in range(1, len(new_state) - 1):
        for j in range(1, len(new_state[0]) - 1):
            if game[i][j] == '.':
                continue
            surrounding_filled_seats = 0
            for k in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if k == i and l == j:
                        continue
                    if game[k][l] == '#':
                        surrounding_filled_seats += 1

            # rules of the game
            if surrounding_filled_seats >= 4:
                new_state[i][j] = 'L'
            elif new_state[i][j] == 'L' and surrounding_filled_seats == 0:
                new_state[i][j] = '#'
            if new_state[i][j] == '#':
                seat_count += 1

    # easier to pass around list of strings instead of
    # list of list (i don't want to deep copy)
    # so convert back to a list of strings
    new_state = [''.join(row) for row in new_state]
    return (seat_count, new_state)
    
def look_left(game, i, j):
    while j > 0:
        j -= 1
        if game[i][j] == '.':
            continue
        if game[i][j] == '#':
            return 1
        return 0
    return 0

def look_right(game, i, j):
    while j < len(game[i])-1:
        j += 1
        if game[i][j] == '.':
            continue
        if game[i][j] == '#':
            return 1
        return 0
    return 0

def look_up(game, i, j):
    while i > 0:
        i -= 1
        if game[i][j] == '.':
            continue
        if game[i][j] == '#':
            return 1
        return 0
    return 0

def look_down(game, i, j):
    while i < len(game) -1:
        i += 1
        if game[i][j] == '.':
            continue
        if game[i][j] == '#':
            return 1
        return 0
    return 0

def look_upleft(game, i, j):
    while i > 0 and j > 0:
        i -= 1
        j -= 1
        if game[i][j] == '.':
            continue
        if game[i][j] == '#':
            return 1
        return 0
    return 0

def look_upright(game, i, j):
    while i > 0 and j < len(game[i])-1:
        i -= 1
        j += 1
        if game[i][j] == '.':
            continue
        if game[i][j] == '#':
            return 1
        return 0
    return 0

def look_downright(game, i, j):
    while i < len(game)-1 and j < len(game[i])-1:
        i += 1
        j += 1
        if game[i][j] == '.':
            continue
        if game[i][j] == '#':
            return 1
        return 0
    return 0

def look_downleft(game, i, j):
    while i < len(game)-1 and j > 0:
        i += 1
        j -= 1
        if game[i][j] == '.':
            continue
        if game[i][j] == '#':
            return 1
        return 0
    return 0

def tick2(game):
    new_state = [list(row) for row in game]
    seat_count = 0
    for i in range(1, len(new_state) - 1):
        for j in range(1, len(new_state[0]) - 1):
            if game[i][j] == '.':
                continue
            surrounding_filled_seats = 0
            surrounding_filled_seats += look_left(game, i, j)
            surrounding_filled_seats += look_right(game, i, j)
            surrounding_filled_seats += look_up(game, i, j)
            surrounding_filled_seats += look_down(game, i, j)
            surrounding_filled_seats += look_upleft(game, i, j)
            surrounding_filled_seats += look_upright(game, i, j)
            surrounding_filled_seats += look_downleft(game, i, j)
            surrounding_filled_seats += look_downright(game, i, j)

            if surrounding_filled_seats >= 5:
                new_state[i][j] = 'L'
            elif new_state[i][j] == 'L' and surrounding_filled_seats == 0:
                new_state[i][j] = '#'
            if new_state[i][j] == '#':
                seat_count += 1

    new_state = [''.join(row) for row in new_state]
    return (seat_count, new_state)

with open('11input1.txt') as f:
    # add . round the rim of the game input so that we can start
    # indices at 1 and do 1-1 without worrying about index errors    
    game = ["." + row + "." for row in f.read().split('\n')]
    game.insert(0, "." * len(game[1]))
    game.append("." * len(game[1]))

    prev_seat_count = -1
    seat_count = 0
    tick_count = 0
    while(True):
        seat_count, game = tick(game)
        tick_count += 1
        if seat_count == prev_seat_count:
            break
        else:
            prev_seat_count = seat_count
    print('Stable seat count == ' + str(seat_count) + ' in ' + str(tick_count) + ' ticks')

    # game has been manipulated by part 1, so gotta reread it
    f.seek(0)
    game = ["." + row + "." for row in f.read().split('\n')]
    game.insert(0, "." * len(game[1]))
    game.append("." * len(game[1]))
    prev_seat_count = -1
    tick_count = 0
    while(True):
        seat_count, game = tick2(game)
        tick_count += 1
        if seat_count == prev_seat_count:
            break
        else:
            prev_seat_count = seat_count
    print('Stable seat count == ' + str(seat_count) + ' in ' + str(tick_count) + ' ticks')