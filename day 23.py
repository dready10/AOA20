# this was the first time i had to use hints to get to 
# an answer. part 1 worked fine (that solution, almost
# entirely optimized for speed is below. the biggest
# slowdown was still list.index, but even without
# list.index, the array deletes and inserts
# would have taken about six hours), but part 2. oh no.

# so instead used a hint for a hybrid linked list/map, which
# was the hint that i found when looking. that way,
# looking up any particular node is O(1) (on average)
# and moving cups is also O(1) (on average). still
# runs awful slow, but it finishes before dinner, so.
class NodeList:
    # we need nodes as a data structure to keep
    # track of the cup value as well as which
    # cup is next in the circle
    class Node: 
        def __init__(self, value, map):
            self.value = value
            self.next = None
            self.map = map

        def setNext(self, node):
            self.next = node
            self.map[self.value] = self

    def __init__(self, nodes):
        self.map = {}
        prev_node = None
        for node in nodes:
            new_node = self.Node(node, self.map)
            self.map[node] = self.Node(node, self.map)
            if prev_node is not None:
                prev_node.setNext(new_node)
            prev_node = new_node

        new_node.setNext(self.currentCup) # link the last element to the first element to form a circle
        self.currentCup = self.map[nodes[0]] # start at the beginning of the circle


    def getCurrentCup(self):
        return self.currentCup
    
    # advances "cursor" in the circle forward one cup
    def nextCup(self):
        self.currentCup = self.currentCup.next
    
    def getNextThreeCupValues(self):
        return [self.currentCup.next.value, self.currentCup.next.next.value, self.currentCup.next.next.next.value]

    # slice three cups after the current cup out of the list and
    # move them to after the cup specified by nodeId
    def moveNextTreeCupsTo(self, nodeId):
        linkCurrentCupToNode = self.currentCup.next.next.next.next
        insertAtNode = self.map[nodeId]
        instertedCupsNextNode = insertAtNode.next

        insertAtNode.setNext(self.currentCup.next)
        insertAtNode.next.next.next.setNext(instertedCupsNextNode)

        self.currentCup.setNext(linkCurrentCupToNode)

def play_game(cups, moves, max_cup):
    for _ in range(moves):
        currentCupVal = cups.getCurrentCup().value
        nextThree = cups.getNextThreeCupValues()

        # find where to insert the three cups
        currentCupVal -= 1
        if currentCupVal == 0:
            currentCupVal = max_cup
        while currentCupVal in nextThree:
            currentCupVal -= 1
            if currentCupVal == 0:
                currentCupVal = max_cup

        # move the cups there and advance the cursor
        cups.moveNextTreeCupsTo(currentCupVal)
        cups.nextCup()

# part 1
cups = [int(n) for n in list('418976235')]
cup_map = NodeList(cups)
play_game(cup_map, 100, 9)
node = cup_map.map[1]
next_node = node.next
s = ''
while next_node != node:
    s += str(next_node.value)
    next_node = next_node.next
print(s)

# part 2
cups = [int(n) for n in list('418976235')]
cups += [i for i in range(10, 1000001)]
cup_map = NodeList(cups)
play_game(cup_map, 10000000, 1000000)
node = cup_map.map[1]
print('{0} = {1} * {2}'.format(node.next.value * node.next.next.value, node.next.value, node.next.next.value))

'''
def shift(l, n):
    new_l = l[0:n]
    del l[0:n]
    return new_l

def get_dest(l, n, max_cup):
    if n == 0:
        n += max_cup
    while n in l:
        n += -1
        if n == 0:
            n += max_cup
    return n

def play_game(cups, moves):
    max_cup = max(cups)
    for _ in range(1, moves+1):
        moved = cups[0]
        picked_up = cups[1:4]
        del cups[0:4]
        dest = get_dest(picked_up, moved-1, max_cup)
        dest = list.index(cups, dest) + 1
        cups[dest:dest] = picked_up
        cups.append(moved)
    return cups

'''