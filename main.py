import numpy as np

from single_pair_graph import UndirGraph
import single_pair_poa
import single_pair_so
import single_pair_ne
import graph_tool as gt
import csv
import itertools

FLOW = 2000
IMG_FILE = 'code/single_pair_code/test.png'
REF_FILE = "og.csv"
CAP_ADJ_FILE = "cap_adj.csv"

g = UndirGraph()
g.draw(IMG_FILE)

# Write costs of traveling across unmodified graph to file
columns = ['OD pair', 'Cost']
with open(REF_FILE, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

entries = []

for pair in itertools.permutations([vertex for vertex in gt.Graph.get_vertices(g.g)], 2):
    a, b = pair
    od_pair = (a, b)

    cost = single_pair_poa.find_cost(a, b, FLOW, g)

    entries.append({'OD pair': od_pair, 'Cost': f'{cost}'})

with open(REF_FILE, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writerows(entries)


# Write costs after capacity adjustments to a separate file
columns = ['Capacity adjustment', 'Edge adjusted', 'OD pair', 'Cost']

with open("cap_adj.csv", 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

cap_adjust = 0.1
for edge in g.get_edges():
    u, v = edge
    edge_adjusted = (u, v)
    g.capacity[edge_adjusted] = g.capacity[edge_adjusted] * cap_adjust
    
    single_pair_poa.find_all_costs(FLOW, cap_adjust, edge_adjusted, g, CAP_ADJ_FILE)

    g.capacity[edge_adjusted] = g.capacity[edge_adjusted] / cap_adjust

