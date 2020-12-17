# I don't use these two variables anywhere, but I keep them as reference.
# Instead of deep copying a grid to another grid (which, thank God I didn't
# do that because it would have been a nightmare in part 2), I "mark" a cell
# for what it becomes at the end of a game tick. So if a cube is visible ('#'),
# but has 0 neighbors on this tick, it should become invisible, so we "mark it"
# with a ','. That way, when counting neighbors, we can count either '#' or ','
# (because the ',' isn't invisible yet, it just will be), and that way we don't
# have to deep copy. Same logic for . > V--we don't want to count Vs because
# they aren't visible in the current tick, but they will be visible after the
# tick ends.
visible_markers = ('#', ',')
invisible_markers = ('.','V')

# utility function, not really necessary
def print_grid(grid):
    for z in range(0, len(grid)):
        print('z = {0}'.format(z))
        for y in range(0, len(grid[0])):
            print(''.join(grid[z][y]))
        print('')

# counts the number of neighbors at coord (x, y, z)
def number_of_neighbors(grid, x, y, z):
    min_x = 0 if x-1 < 0 else x-1
    min_y = 0 if y-1 < 0 else y-1
    min_z = 0 if z-1 < 0 else z-1

    max_x = x + 2 if x + 2 < len(grid[0][0]) else len(grid[0][0])
    max_y = y + 2 if y + 2 < len(grid[0]) else len(grid[0])
    max_z = z + 2 if z + 2 < len(grid) else len(grid)

    number_of_neighbors = 0
    for _z in range(min_z, max_z):
        for _y in range(min_y, max_y):
            number_of_neighbors += grid[_z][_y][min_x:max_x].count('#')
            number_of_neighbors += grid[_z][_y][min_x:max_x].count(',')

    if (grid[z][y][x] == '#'):
        number_of_neighbors -= 1
    
    return number_of_neighbors

# when looking in a tick if a cube needs to become visible, we also need
# to check spaces outside the "current" cube. eg, we need to check the 
# neightbors of (-1, -1, -1) to see if it flips. to do so, we always make sure
# the cube is surrounded with .s, so that the tick can run number_of_neighbors
# on them.
def expand_grid(grid):
    # if the "top" of the cube has any active cells (#), insert a layer on top 
    if str(grid[0]).count('#') > 0:
        grid.insert(0, [list('.'*len(grid[0][0])) for line in grid[0]])
    # if the "bottom" of the cube has any active cells, append a layer on the bottom
    if str(grid[len(grid)-1]).count('#') > 0:
        grid.append([list('.'*len(grid[0][0])) for line in grid[0]])

    # if the "back" of the cube has any active cells, insert a side on the back side
    expand = False
    for z in range(0, len(grid)):
        if str(grid[z][0]).count('#') > 0:
            expand = True
            break
    if expand == True:
        for z in range(0, len(grid)):
            grid[z].insert(0, list('.' * len(grid[0][0])))

    # if the "front" of the cube has any active cells, append a side on the front
    expand = False
    for z in range(0, len(grid)):
        if str(grid[z][len(grid[z])-1]).count('#') > 0:
            expand = True
            break
    if expand == True:
        for z in range(0, len(grid)):
            grid[z].append(list('.' * len(grid[0][0])))

    # if the "left" of the cube has any active cells... you know the drill
    expand = False
    for z in range(0, len(grid)):
        if expand == True:
            break
        for y in range(0, len(grid[0])):
            if grid[z][y][0] == '#':
                expand = True
                break
    if expand == True:
        for z in range(0, len(grid)):
            for y in range(0, len(grid[0])):
                grid[z][y].insert(0, '.')

    # now for the right side
    expand = False
    for z in range(0, len(grid)):
        if expand == True:
            break
        for y in range(0, len(grid[0])):
            if grid[z][y][len(grid[0][0]) - 1] == '#':
                expand = True
                break
    if expand == True:
        for z in range(0, len(grid)):
            for y in range(0, len(grid[0])):
                grid[z][y].append('.')

# do the game, pretty self-explanatory
def tick(grid):
    for z in range(0, len(grid)):
        for y in range(0, len(grid[0])):
            for x in range(0, len(grid[0][0])):
                neighbors = number_of_neighbors(grid, x, y, z)
                if grid[z][y][x] == '#':
                    if neighbors != 2 and neighbors != 3:
                        grid[z][y][x] = ','
                else:
                    if neighbors == 3:
                        grid[z][y][x] = 'V'
    
    for z in range(0, len(grid)):
        for y in range(0, len(grid[0])):
            for x in range(0, len(grid[0][0])):
                if grid[z][y][x] == 'V':
                    grid[z][y][x] = '#'
                if grid[z][y][x] == ',':
                    grid[z][y][x] = '.'

    expand_grid(grid)

with open('17input1.txt') as f:
    grid = [[list(line) for line in f.read().split()]]
    expand_grid(grid)

    for i in range(0, 6):
        tick(grid)

    active_cells = 0
    for z in range(0, len(grid)):
        for y in range(0, len(grid[0])):
            active_cells += grid[z][y].count('#')
    print(active_cells)

    from collections import defaultdict

# starting part 2 with another utility function.
def print_grid_2(grid):
    for w in range(0, len(grid)):
        for z in range(0, len(grid[0])):
            print('z = {0}, w = {1}'.format(z, w))
            for y in range(0, len(grid[0][0])):
                print(''.join(grid[w][z][y]))
            print('')

# same algorithm as above, just with one more layer.
def number_of_neighbors_2(grid, x, y, z, w):
    min_x = 0 if x-1 < 0 else x-1
    min_y = 0 if y-1 < 0 else y-1
    min_z = 0 if z-1 < 0 else z-1
    min_w = 0 if w-1 < 0 else w-1

    max_x = x + 2 if x + 2 < len(grid[0][0][0]) else len(grid[0][0][0])
    max_y = y + 2 if y + 2 < len(grid[0][0]) else len(grid[0][0])
    max_z = z + 2 if z + 2 < len(grid[0]) else len(grid[0])
    max_w = w + 2 if w + 2 < len(grid) else len(grid)

    number_of_neighbors = 0
    for _w in range(min_w, max_w):
        for _z in range(min_z, max_z):
            for _y in range(min_y, max_y):
                number_of_neighbors += grid[_w][_z][_y][min_x:max_x].count('#')
                number_of_neighbors += grid[_w][_z][_y][min_x:max_x].count(',')

    if (grid[w][z][y][x] == '#'):
        number_of_neighbors -= 1
    
    return number_of_neighbors

def expand_grid_2(grid):
    # so basically, expand_grid did the following: inserted . for every x.y in z = 0 and z = max(z)
    # and . for every z,x in y = 0 and y = max(y)
    # and . for every z,y in x = 0 and x = max(x)

    # so. similarly. insert a . for every x,y,z in w = 0 and max(w),
    # . for every x, y, w in z = 0 and max(z)
    # . for every x, z, w in y = 0 and max(y)
    # . for every y, z, w in x = 0 and max(x)

    # in expand_grid, i checked whether expansion was necesssary (eg if "current face" had a '#'
    # and therefore if we needed to expand the cube so it was again surrounded by '.').
    # here, i'm not checking because it's six ticks.
    # (in part 1, the checking could have been important in part 2)        

    # finally, what is 'for i in range(0, 2)' about, and the 'if i == 0'? well, when
    # you generate a list of lists and then append that to both ends of an array,
    # you're actually appending a pointer to the list... so if you mutate the list,
    # you mutate both ends of the list when probably you only meant to mutate one end.
    # could i have used copy.deepcopy? probably, and it'd probably be faster, too.
    # but, six ticks.

    for i in range(0, 2):
        new_cube = []
        for z in range(0, len(grid[0])):
            new_y = []
            for y in range(0, len(grid[0][0])):
                new_y.append(list('.' * len(grid[0][0][0])))
            new_cube.append(new_y)
        if i == 0:
            grid.insert(0, new_cube)
        else: 
            grid.append(new_cube)

    for w in range(0, len(grid)):
        for i in range(0, 2):
            new_square = []
            for y in range(0, len(grid[0][0])):
                new_square.append(list('.' * len(grid[0][0][0])))
            if i == 0:
                grid[w].insert(0, new_square)
            else:
                grid[w].append(new_square)

    for w in range(0, len(grid)):
        for z in range(0, len(grid[0])):
            for i in range(0, 2):
                new_y = list('.' * len(grid[0][0][0]))
                if i == 0:
                    grid[w][z].insert(0, new_y)
                else:
                    grid[w][z].append(new_y)

    for w in range(0, len(grid)):
        for z in range(0, len(grid[0])):
            for y in range(0, len(grid[0][0])):
                grid[w][z][y].insert(0, '.')
                grid[w][z][y].append('.')

# same as tick, just add one more layer.
def tick_2(grid):
    for w in range(0, len(grid)):
        for z in range(0, len(grid[0])):
            for y in range(0, len(grid[0][0])):
                for x in range(0, len(grid[0][0][0])):
                    neighbors = number_of_neighbors_2(grid, x, y, z, w)
                    if grid[w][z][y][x] == '#':
                        if neighbors != 2 and neighbors != 3:
                            grid[w][z][y][x] = ','
                    else:
                        if neighbors == 3:
                            grid[w][z][y][x] = 'V'

    for w in range(0, len(grid)):    
        for z in range(0, len(grid[0])):
            for y in range(0, len(grid[0][0])):
                for x in range(0, len(grid[0][0][0])):
                    if grid[w][z][y][x] == 'V':
                        grid[w][z][y][x] = '#'
                    if grid[w][z][y][x] == ',':
                        grid[w][z][y][x] = '.'

    expand_grid_2(grid)

with open('17input1.txt') as f:
    grid = [[[list(line) for line in f.read().split()]]]
    expand_grid_2(grid)

    for i in range(0, 6):
        tick_2(grid)

    active_cells = 0
    for w in range(0, len(grid)):
        for z in range(0, len(grid[0])):
            for y in range(0, len(grid[0][0])):
                active_cells += grid[w][z][y].count('#')
                                
    print(active_cells)