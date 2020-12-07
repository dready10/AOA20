class Graph:
    def __init__(self):
        self.nodes = {}
        self.node_count = 0
        self.edges = []

    # for matrix representation of edges, each node needs an id. so ids
    # (self.node_count) are handed out sequentially and stored in
    # a dict (self.nodes) for id look up
    def add_node(self, node_name):
        self.nodes[node_name] = self.node_count
        self.node_count += 1
        for edge in self.edges:
            edge.append(0)
        self.edges.append([0 for i in range(self.node_count)])
    
    # edges are represented in a matrix. a row is child nodes, a column is parent nodes
    def add_edge(self, parent, child, weight):
        parent_place = self.nodes[parent]
        child_place = self.nodes[child]
        self.edges[parent_place][child_place] = weight

    # helper for readability
    def get_node_id(self, node_name):
        return self.nodes[node_name]

    # we want to know how many bags can eventually contain a shiny gold bag. in this
    # directed graph, the "parent bag" in an edge contains the child.
    # if we start at the child, we can see which exact bags hold the child. then, 
    # we visit each parent and see what their grandparents are (they hold child, too)
    # and so on. the question is what bags hold the shiny gold bag (ie: which unique
    # nodes hold the child), so we don't want to just count edges otherwise a grandparent
    # could count as two (eg: red > black > gold, red > green > gold is three nodes,
    # but you would visit red twice)
    def get_connected_parent_nodes(self, node_id):
        visited_nodes = set([node_id])
        edges = [row[node_id] for row in self.edges]
        for i, edgeweight in enumerate(edges):
            if edgeweight > 0:
                visited_nodes = visited_nodes.union(self.get_connected_parent_nodes(i))
        return visited_nodes

    # here we do want to count edges (with their weights). if a gold bag (parent)
    # contains 6 black bags a 2 green, that 6 * 1 black bag + 2 * 1 green.
    # if the black/green bags contains nothing, great.
    # but if the black bag contains 2 red bags, then we need to figure the
    # weight of the black bag--in this case, 1 (the bag itself) + 2*1.
    # if the green bag ALSO contains 2 red, do the same thing (count those edges)
    # so then the gold contains 6 * 3 black bag + 2 * 3 green = weight of 24.
    def get_connected_children_weight(self, node_id):
        weight = 1
        for i, edgeweight in enumerate(self.edges[node_id]):
            if edgeweight > 0:
                weight += edgeweight * self.get_connected_children_weight(i)
        return weight

# parsing helper
def get_edge_data(child):
    c = child.split(' ')
    childname = ' '.join([c[1], c[2]])
    if c[0] == 'no': #empty bags don't add an edge to the edge matrix
        return [0,""]
    return [c[0], childname] #weight, childname

#parsing helper
def make_node_name(name):
    n = name.split(' ')
    return ' '.join([n[0], n[1]])

with open('7input1.txt', 'r') as f:
    rules = [rule.split(' contain ') for rule in f.read().split('\n')]
    
    g = Graph()
    #give each node an id
    for rule in rules:
        g.add_node(make_node_name(rule[0]))

    #populate the edges
    for rule in rules:
        parent = make_node_name(rule[0])
        edges = rule[1].split(', ')
        for edge in edges:
            weight, childname = get_edge_data(edge)
            if int(weight) > 0:
                g.add_edge(parent, childname, int(weight))

    #part 1
    # (-1 because we don't count the gold bag as containing itself)
    print(len(g.get_connected_parent_nodes(g.get_node_id("shiny gold"))) - 1)

    #part 2
    # (-1 because the gold bag itself isn't included in the weight)
    print(g.get_connected_children_weight(g.get_node_id("shiny gold")) - 1)
    