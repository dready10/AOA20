with open('10input1.txt') as f:
    adapters = [int(i) for i in f.read().split()]
    adapters.sort()

    onejump = 0
    threejump = 0
    prevjoltage = 0
    for adapter in adapters:
        if adapter - prevjoltage == 1:
            onejump +=1
        if adapter - prevjoltage == 3:
            threejump += 1
        prevjoltage = adapter

    threejump += 1
    print(threejump * onejump)

    # part2
    # so here's the theory here: at each adapter, we need to count how many different ways
    # we could get there. in a graph of 0 > 1 > 4 > 7 > 10, there's clearly one path.

    # in a graph of 0 > 1 > 4 > 5 > 6 > 7 > 10 > 12 , there's a few paths. Here's what we do:
    # at each node, find the notes that we can jump from to get to the current node. for node 1 (1), there's 
    # only one way to get there. for node 2 (4), there's only one way to get there
    # for node 3 (5), there's still only one way to get there. for node 4 (6), there are
    # 2 ways--include or exclude node 3 (5). for node 5 (7), there's three ways to get there,
    # through nodes 2, 3, and 4. but, there are two ways to go through node 4! so to get to node 5, there's
    # four ways to get there: 1 node 2 path, 1 node 3 path, and 2 node 4 paths, for 4 paths to
    # get to node 5. then, for node 6 (10), there's only one way to get there (through 5),
    # but to get to node 5, there are 4 ways, so there's also 4 ways to get to node 6.

    # the graph that really helped me figure this out was at 
    # https://en.wikipedia.org/wiki/Directed_acyclic_graph#/media/File:Topological_Ordering.svg
    # using the sample sets to draw this graph and manually going through the above, process
    # really helped me understand it

    # precompute the first three steps (this could be more elegant, probably, but
    # i have spent enough time on this today as it is...)
    paths_to_reach = [1] # only 1 way to reach node 1
    if (adapters[1] < 3):
        paths_to_reach.append(2) #if node 2 is less than 3, you can reach it through node 1, or directly
    else:
        paths_to_reach.append(1) #if it's not less than 3, you can only reach it through node 1
    if (adapters[2] <= 3):
        # if node 3 is less than 3, there's 3 or 4 ways you can reach it:
        # directly
        # from node 1 (which can only be access one way)
        # from node 2 (which might be optionally accessible from node 2--two ways or 1 way)
        paths_to_reach.append(paths_to_reach[1] + 1 + 1)
    else:
        # otherwise, you can only reach node 3 through nodes 1 or 2, similar logic as above
        # with node 2 possibly having 1 or 2 ways to reach it.
        if(adapters[2] - adapters[0]) <= 3: 
            paths_to_reach.append(paths_to_reach[1] + 1)
        else:
            paths_to_reach.append(paths_to_reach[1])

    # now go through each node, and look back at the nodes that can
    # get you to the current node, and add up the ways to get to
    # the current node through the previous nodes
    for i, adapter in enumerate(adapters[3:]):
        i += 3
        paths_for_i = paths_to_reach[-1]
        if(adapters[i] - adapters[i-2]) <= 3:
            paths_for_i += paths_to_reach[i-2]
        if (adapters[i] - adapters[i-3]) <= 3:
            paths_for_i += paths_to_reach[i-3]
        paths_to_reach.append(paths_for_i)

    print(paths_to_reach[-1])