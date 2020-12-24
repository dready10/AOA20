# pretty straightforward puzzle.

with open('24input1.txt','r') as f:
    tiles = f.read().split('\n')
    black_tiles = []

    # from any tile, these are the coordinate steps you can take--east is x+2, y+0, ne
    # is x+1, y+1, etc.
    steps = {'e': (2,0), 'w': (-2,0), 'ne': (1,1), 'nw':(-1,1), 'se': (1, -1), 'sw': (-1, -1) }

    # part 1
    # for each line:
    # parse the line. an n or s is always followed by an e or w,
    # so when you encounter those, pop an extra character. then,
    # add +x and +y of the steps dict to our location to "take"
    # that step.
    for tile in tiles:
        loc = [0,0]
        tile = list(tile)
        while len(tile) > 0:
            d = tile.pop(0)
            if d == 'n' or d == 's':
                d += tile.pop(0)
            loc[0] += steps[d][0]
            loc[1] += steps[d][1]
        # when there are no more steps in that tile,
        # flip it.
        if loc in black_tiles:
            black_tiles.remove(loc)
        else:
            black_tiles.append(loc)
    print(len(black_tiles))

    # part 2
    # i took this model from when of the solutions i read
    # after i finished day 17, conway cubes. for each
    # black tile, enumerate their neighbors. keep
    # track of how often they've been enumerated  
    black_tiles = [tuple(tile) for tile in black_tiles]
    for d in range(100):
        neighbors = {}
        for tile in black_tiles:
            for step in steps:
                k = tuple([x + y for x,y in zip(steps[step], tile)])
                if k in neighbors:
                    neighbors[k] += 1
                else:
                    neighbors[k] = 1

        # then, for each neighbor, if it's white, flip
        # it black if it appeared in the above enumeration
        # twice (eg: it has two black neighbors)
        flip_whites = []
        for neighbor in neighbors:
            if neighbors[neighbor] == 2 and neighbor not in black_tiles:
                flip_whites.append(neighbor)

        # if it's black, drop the tile if it has 0 or 3+ black neighbors
        keep_blacks = []
        for tile in black_tiles:
            if tile in neighbors and neighbors[tile] <= 2:
                keep_blacks.append(tile)
        
        # "do" the flip
        black_tiles = flip_whites + keep_blacks

    # this takes about ten seconds to run. not ideal, but good enough.
    print(f'Day {d + 1}: {len(black_tiles)}')