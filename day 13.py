from functools import reduce

with open('13input1.txt', 'r') as f:
    time = int(f.readline())
    schedule = [line for line in f.readline().split(',')]
    lines = [int(line) for line in schedule if line != 'x']

    # part 1
    arrivals = [(int(line)-time % int(line)) for line in schedule if line != 'x']
    print(lines[arrivals.index(min(arrivals))] * min(arrivals))
    
    # part 2

    current_time = 0 
    cycle_length = lines[0]
    current_cycle = 1

    # for each line, find the departure time that is cycle_offset away from a multiple of the current cycle length
    # what is the logic here?
    # for lines 17, x, 13, 19: 17 and 13 (with offset 2) share a departure time of 102. that means that every instance of 102 + 17*13*n
    # will also be a common time for those lines, so, starting with 102, we step forward 17*13 to find the time (with offset 3) that
    # works for line 19. 102 + 17*13*(cycle = 15) = 3417, which satisfies (3417+3)%19 = 0
    # if there were another line (23, eg), then, starting at time 3417, we'd step forward 17*13*19 each cycle
    # to find the common time (with offset 4) that works for line 23.
    for line in lines[1:]:
        cycle_offset = schedule.index(str(line))
        current_cycle = 1
        while True:
            if (current_time + cycle_offset + current_cycle * cycle_length) % line == 0:
                current_time += current_cycle * cycle_length
                cycle_length *= line
                break
            current_cycle += 1

    print(current_time)