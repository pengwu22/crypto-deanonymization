

filePre = "../../danning/joint_total_"


def parse_user_edge(line):
    fields = line.rstrip('\n').split(',')
    return fields[0], fields[1], float(fields[2])
def parse_user_node(line):
    fields = line.rstrip('\n').split(',')
    return (fields[0], fields[1])

import networkx as nx
G = nx.DiGraph()
with open(filePre + "edge.csv") as f:
    G.add_weighted_edges_from(map(parse_user_edge, f))

count = 0
mappings = {}
for n in G.nodes():
    successors = G.successors(n)
    if successors == G.predecessors(n) and len(successors) == 1 and n not in successors:
        # n is thus a node that can be shrinked.
        count += 1
        mappings[n] = successors[0]

keys = mappings.keys()
for k, v in mappings.items():
    if k in keys:
        if v in keys:
            del mappings[v]
            keys.remove(v)

print count, len(G.nodes()), len(mappings)

print mappings

from collections import Counter
print Counter(mappings.values())




