from math import prod, sqrt

# helper function for part 2. just goes to each coordinate and adds the coords of #s that are in a monster
# to check whether a monster is at that coordinate.
def find_monsters(seamap):
    monster = [(0,18), (1,0), (1,5), (1,6), (1,11), (1,12), (1,17), (1,18), (1,19), (2,1), (2, 4), (2,7), (2,10), (2,13), (2,16)]
    monster_locations = []
    for i in range(len(seamap)):
        if i >= (len(seamap) - 2):
            break
        for j in range(0, len(seamap[0]) - 20):
            is_monster_coord = True
            for x, y in monster:
                t = seamap[i+x][j+y]
                if t != '#':
                    is_monster_coord = False
                    break
            if is_monster_coord:
                monster_locations.append((i,j))
    return monster_locations

# using primes to get a unique identifier for an edge.
# zipping the primes with an edge and multiplying
# by 1 if ., prime if otherwise produces a unique
# id for each edge we can use to match up tile edges
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
def get_edge_id(row):
    return prod([int(x * ((1/x) if y == '.' else 1)) for x, y in zip(primes, row)])

def rotate_left(tile):
    new_tile = [list(r) for r in tile]
    for row in new_tile:
        row.reverse()
    for i in range(len(new_tile)):
        for j in range(i):
            new_tile[i][j], new_tile[j][i] = new_tile[j][i], new_tile[i][j]
    for i, row in enumerate(new_tile):
        new_tile[i] = ''.join(row)
    return new_tile

def rotate_right(tile):
    # lol
    for i in range(0,3):
        tile = rotate_left(tile)
    return tile
    
with open('20input1.txt') as f:
    squares = [square.split('\n') for square in f.read().split('\n\n')]
    tiles = {}
    for tile in squares:
        tiles[tile[0].split(' ')[1][0:-1]] = tile[1:]

    # create the unique ID for each edge. tiles can be flipped
    # so I also have to get the prime for the reversed edge ([::-1])
    tile_edges = {}
    for tile in tiles:
        tile_edges[tile] = []
        # top edge ids
        tile_edges[tile].append(get_edge_id(tiles[tile][0]))
        tile_edges[tile].append(get_edge_id(tiles[tile][0][::-1]))

        # bottom edge ids
        tile_edges[tile].append(get_edge_id(tiles[tile][-1]))
        tile_edges[tile].append(get_edge_id(tiles[tile][-1][::-1]))

        left_edge = [c[0] for c in tiles[tile]]
        right_edge = [c[-1] for c in tiles[tile]]
        tile_edges[tile].append(get_edge_id(left_edge))
        tile_edges[tile].append(get_edge_id(left_edge[::-1]))
        tile_edges[tile].append(get_edge_id(right_edge))
        tile_edges[tile].append(get_edge_id(right_edge[::-1]))


    # great. now we need to data-wrangle. here we want to
    # get the list of tiles attached to each edge--ie, which
    # tiles share an edge
    existing_exteriors = {}
    for tile in tile_edges:
        for edge in tile_edges[tile]:
            if edge not in existing_exteriors.keys():
                existing_exteriors[edge] = [tile]
            else:
                existing_exteriors[edge].append(tile)

    # great. now, for each tile's edge, count the number
    # of each tiles attached to that edge
    tile_matching_edge_counts = {}
    for tile in tile_edges:
        tile_matching_edge_counts[tile] = []
        for edge in tile_edges[tile]:
            tile_matching_edge_counts[tile].append(len(existing_exteriors[edge]))

    # here we'll have ended up with a dictionary of
    # tiles to how many other tiles their edges match.
    # if there's a 1, that means that edge doesn't match
    # any other tile; a 2+ means it matches 2+ tiles.
    # as well, because each tile can both be flipped,
    # the eg top edge (represented twice, forward and in reverse)
    # will, if it matches another tile, show as 2 twice--because that
    # other tile's bottom edge will match it forward and in reverse.
    # corner tiles only match two other tiles, so we're looking
    # for a tile total of 12--1 for each edge*2 for backwards + 4 more
    # for the two matching edges
    res = 1
    for tile in tile_matching_edge_counts:
        if sum(tile_matching_edge_counts[tile])-8 == 4:
            res *= int(tile)
    print(res)
    
    # part 2
    # damn. we do actually have to build the grid. ok. we have the corner tiles...
    # but if they can be flipped in any way, there's no way to tell where
    # which corner they live in... which actually i guess is the point?
    # like you can always rotate a or flip an actual puzzle and then the top
    # left corner is in the bottom right.

    # ok. so with that insight, if we choose one of the tiles and make it the top
    # left then we can figure out which tiles are supposed to be next to it and
    # in which orientation. then we can keep doing that until we have our
    # mosaic. then i guess we have to "orient it" again the right way 
    # so we can do our sea monster search. ok, that's fine this is fine.

    mosaic = []
    for i in range(0, int(sqrt(len(tiles)))):
        mosaic.append([0 for j in range(0, int(sqrt(len(tiles))))])
    mosaic_tile_ids = []
    for i in range(0, int(sqrt(len(tiles)))):
        mosaic_tile_ids.append([0 for j in range(0, int(sqrt(len(tiles))))])

    # the first tile corner tile in our tile heap will become the upper left.
    for tile in tile_matching_edge_counts:
        if sum(tile_matching_edge_counts[tile])-8 == 4:
            break

    # we got our upper left tile. now lets make sure it is oriented.
    # if it's in the upper left, the top edge (tile_edges[tile][0])
    # should be 1 (no matches tiles on that edge). same story with
    # the left side (tile_edges[tile][5])
    if len(existing_exteriors[tile_edges[tile][0]]) > 1:
        tiles[tile].reverse()
    if len(existing_exteriors[tile_edges[tile][4]]) > 1:
        tiles[tile] = [row[::-1] for row in tiles[tile]]

    mosaic_tile_ids[0][0] = tile
    mosaic[0][0] = tiles[tile]

    # great, now that we "know" the right side and bottom sides, 
    # we can start throwing new puzzle pieces on. i go row
    # by row.
    for row in range(0, len(mosaic)):
        for col in range(0, len(mosaic[0])-1):
            current_tile = mosaic[row][col]
            current_tile_id = mosaic_tile_ids[row][col]
            tile_right_id = get_edge_id([r[-1] for r in current_tile])
            if existing_exteriors[tile_right_id][0] == current_tile_id:
                next_tile_id = existing_exteriors[tile_right_id][1]
            else:
                next_tile_id = existing_exteriors[tile_right_id][0]
            next_tile = tiles[next_tile_id]
            
            # ok, now which way do we need to flip the next tile?
            top_next_tile = get_edge_id(next_tile[0])
            top_next_tile_r = get_edge_id(next_tile[0][::-1])
            bottom_next_tile = get_edge_id(next_tile[-1])
            bottom_next_tile_r = get_edge_id(next_tile[-1][::-1])
            left_next_tile = get_edge_id([r[0] for r in next_tile])
            left_next_tile_r = get_edge_id([r[0] for r in next_tile[::-1]])
            right_next_tile = get_edge_id([r[-1] for r in next_tile])
            right_next_tile_r = get_edge_id([r[-1] for r in next_tile[::-1]])

            mosaic_tile_ids[row][col+1] = next_tile_id
            if tile_right_id == left_next_tile:
                mosaic[row][col+1] = next_tile
            elif tile_right_id == left_next_tile_r:
                mosaic[row][col+1] = next_tile[::-1]
            elif tile_right_id == right_next_tile:
                mosaic[row][col+1] = [r[::-1] for r in next_tile]
            elif tile_right_id == right_next_tile_r:
                mosaic[row][col+1] = [r[::-1] for r in next_tile[::-1]]
            elif tile_right_id == top_next_tile:
                mosaic[row][col+1] = rotate_left(next_tile)[::-1]
            elif tile_right_id == top_next_tile_r:
                mosaic[row][col+1] = rotate_left(next_tile)
            elif tile_right_id == bottom_next_tile:
                mosaic[row][col+1] = rotate_right(next_tile)
            elif tile_right_id == bottom_next_tile_r:
                mosaic[row][col+1] = rotate_right(next_tile)[::-1]
            else:
                print('ruh roh')

        if row == len(mosaic)-1:
            break

        # ok, the row is done, now we need to lay down the first tile in the next row
        # this code is basically the same as above, because I am lazy.
        current_tile = mosaic[row][0]
        current_tile_id = mosaic_tile_ids[row][0]
        tile_bottom_id = get_edge_id(current_tile[-1])

        if existing_exteriors[tile_bottom_id][0] == current_tile_id:
            next_tile_id = existing_exteriors[tile_bottom_id][1]
        else:
            next_tile_id = existing_exteriors[tile_bottom_id][0]
        next_tile = tiles[next_tile_id]

        top_next_tile = get_edge_id(next_tile[0])
        top_next_tile_r = get_edge_id(next_tile[0][::-1])
        bottom_next_tile = get_edge_id(next_tile[-1])
        bottom_next_tile_r = get_edge_id(next_tile[-1][::-1])
        left_next_tile = get_edge_id([r[0] for r in next_tile])
        left_next_tile_r = get_edge_id([r[0] for r in next_tile[::-1]])
        right_next_tile = get_edge_id([r[-1] for r in next_tile])
        right_next_tile_r = get_edge_id([r[-1] for r in next_tile[::-1]])

        mosaic_tile_ids[row+1][0] = next_tile_id
        if tile_bottom_id == top_next_tile:
            mosaic[row+1][0] = next_tile
        elif tile_bottom_id == top_next_tile_r:
            mosaic[row+1][0] = [r[::-1] for r in next_tile]
        elif tile_bottom_id == bottom_next_tile:
            mosaic[row+1][0] = next_tile[::-1]
        elif tile_bottom_id == bottom_next_tile_r:
            mosaic[row+1][0] = [r[::-1] for r in next_tile[::-1]]
        elif tile_bottom_id == left_next_tile:
            mosaic[row+1][0] = [r[::-1] for r in rotate_right(next_tile)]
        elif tile_bottom_id == left_next_tile_r:
            mosaic[row+1][0] = rotate_right(next_tile)
        elif tile_bottom_id == right_next_tile:
            mosaic[row+1][0] = rotate_left(next_tile)
        elif tile_bottom_id == right_next_tile_r:
            mosaic[row+1][0] = rotate_left(next_tile)[::-1]
        else:
            print('ruh roh 2')

    # great. we have our grid. now lets combine it all up into one big array of strings.
    # start by stripping the boarders.
    for i, row in enumerate(mosaic):
        for j, tile in enumerate(row):
            tile = tile[1:-1]
            for k, tr in enumerate(tile):
                tile[k] = tr[1:-1]
            row[j] = tile
        mosaic[i] = row

    # ok, now we'll create a seamap, so it's a simple 2d array
    seamap = []
    for tile_row in mosaic:
        for row in range(len(tile_row[0])):
            longRow = ''
            for tile in tile_row:
                if tile != 0:
                    longRow += tile[row]
            seamap.append(list(longRow))
    
    # find the monsters, but we might have to flip or rotate
    # the map to find them, so keep trying to find them
    # until we get the right orientation.
    monsters = find_monsters(seamap)
    count = 1
    while len(monsters) == 0:
        seamap = rotate_left(seamap)
        monsters = find_monsters(seamap)
        count += 1
        if count == 4:
            seamap = [r[::-1] for r in seamap]

    # i am sure there is a smarter way to do this, but
    # i just want to be done.
    totalpounds = 0
    for r in seamap:
        for c in r:
            if c == '#':
                totalpounds += 1
    totalpounds -= len(monsters) * 15
    print(totalpounds)
