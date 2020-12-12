# part 1
orientations = [
    [1, 0], # east
    [0, -1], # north
    [-1, 0], # west
    [0, 1] # south
]

with open('12input1.txt') as f:
    commands = [command for command in f.read().split('\n')]
    position = [0, 0]
    orientation = 0
    
    for command in commands:
        order = command[0]
        movement = int(command[1:])
        if order == 'F':
            movement = [a * movement for a in orientations[orientation]]
        if order == 'E':
            movement = [a * movement for a in orientations[0]]
        if order == 'N':
            movement = [a * movement for a in orientations[1]]
        if order == 'W':
            movement = [a * movement for a in orientations[2]]
        if order == 'S':
            movement = [a * movement for a in orientations[3]]
        if order == 'R':
            orientation = (orientation - int(movement / 90)) % 4
            movement = [0, 0]
        if order == 'L':
            orientation = (orientation + int(movement / 90)) % 4
            movement = [0, 0]

        position = [a+b for a,b in zip(position, movement)]


    print('final position: ' + str(position))
    print('manhattan distance: ' + str(abs(position[0]) + abs(position[1])))

# part 2
    ship_position = [0, 0]
    waypoint_position = [10, -1]
    
    for command in commands:
        order = command[0]
        movement = int(command[1:])
        if order == 'F':
            movement = [a * movement for a in waypoint_position]
            ship_position = [a+b for a,b in zip(ship_position, movement)]
            movement = [0,0] # we don't want to move the waypoint further down
        if order == 'E':
            movement = [a * movement for a in orientations[0]]
        if order == 'N':
            movement = [a * movement for a in orientations[1]]
        if order == 'W':
            movement = [a * movement for a in orientations[2]]
        if order == 'S':
            movement = [a * movement for a in orientations[3]]
        if order == 'R':
            if movement == 180:
                waypoint_position = [-waypoint_position[0], -waypoint_position[1]]
            elif movement == 90:
                waypoint_position = [-waypoint_position[1], waypoint_position[0]]
            elif movement == 270:
                waypoint_position = [waypoint_position[1], -waypoint_position[0]]
            else:
                print('ruh roh, unexpected turn movement: ' + str(movement))
            movement = [0,0] # we don't want to move the way point
        if order == 'L':
            if movement == 180:
                waypoint_position = [-waypoint_position[0], -waypoint_position[1]]
            elif movement == 90:
                waypoint_position = [waypoint_position[1], -waypoint_position[0]]
            elif movement == 270:
                waypoint_position = [-waypoint_position[1], waypoint_position[0]]
            else:
                print('ruh roh, unexpected turn movement: ' + str(movement))
            movement = [0,0] # sameeeeee
        waypoint_position = [a+b for a,b in zip(waypoint_position, movement)]

    print('final ship position: ' + str(ship_position))
    print('final waypoint position: ' + str(waypoint_position))
    print('manhattan distance: ' + str(abs(ship_position[0]) + abs(ship_position[1])))