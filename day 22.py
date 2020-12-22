# for ease of keeping track of game states that have already happened
def hash_round(player1deck, player2deck):
    return hash((tuple(player1deck), tuple(player2deck)))

# for part 2. basically the same structure as part 1.
def recursively_play(player1deck, player2deck):
    round_hashes = [] # list of game states
    while len(player1deck) > 0 and len(player2deck) > 0:

        # if the game state of this sub-game has already happened,
        # player 1 wins, per the rules. otherwise, add this game
        # state to the list of occurred-states.
        round_hash = hash_round(player1deck, player2deck)
        if round_hash in round_hashes:
            return 1, player1deck
        else:
            round_hashes.append(round_hash)

        # play the game. if there are enough cards to recurse, do so.
        # otherwise, the player with the highest card wins.
        p1play, p2play = player1deck.pop(0), player2deck.pop(0)
        if len(player1deck) >= p1play and len(player2deck) >= p2play:
            player, winner = recursively_play(player1deck[0:p1play], player2deck[0:p2play])
            if player == 1:
                player1deck.append(p1play)
                player1deck.append(p2play)
            else:
                player2deck.append(p2play)
                player2deck.append(p1play)
        elif p1play > p2play:
            player1deck.append(p1play)
            player1deck.append(p2play)
        else:
            player2deck.append(p2play)
            player2deck.append(p1play)

    # we have a winner.
    winning_player = 1 if len(player1deck) > 0 else 2
    winning_deck = player1deck if len(player1deck) > 0 else player2deck

    return winning_player, winning_deck

with open('22input1.txt', 'r') as f:
    player1deckS, player2deckS = f.read().split('\n\n') #deckS to store for part 2
    player1deck = [int(x) for x in player1deckS.split('\n')[1:]]
    player2deck = [int(x) for x in player2deckS.split('\n')[1:]]

    # should be pretty self-explanatory...
    while len(player1deck) > 0 and len(player2deck) > 0:
        p1play, p2play = player1deck.pop(0), player2deck.pop(0)

        if p1play > p2play:
            player1deck.append(p1play)
            player1deck.append(p2play)
        else:
            player2deck.append(p2play)
            player2deck.append(p1play)
    winner = player1deck if len(player1deck) > 0 else player2deck

    print(sum([x*y for x, y in zip(winner, reversed(range(1,len(winner)+1)))]))

    # part 2
    player1deck = [int(x) for x in player1deckS.split('\n')[1:]]
    player2deck = [int(x) for x in player2deckS.split('\n')[1:]]

    winner, winning_deck = recursively_play(player1deck, player2deck)

    print(sum([x*y for x, y in zip(winning_deck, reversed(range(1,len(winning_deck)+1)))]))