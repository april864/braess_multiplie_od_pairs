import graph_tool.all as gt
import scipy
import numpy as np
import csv
import single_pair_so
import single_pair_ne
from single_pair_graph import UndirGraph
import itertools


## Function to find price of anarchy
def find_poa(origin: int, destination: int, total_flow: int, graph: UndirGraph):

    paths_list = graph.list_of_paths(origin, destination)

    so_flows = single_pair_so.find_optimal_int_flows(origin, destination, total_flow, graph)
    so_times = list(graph.find_path_travel_times(so_flows, paths_list).values())

    ne_flows = single_pair_ne.get_NE_flows(origin, destination, total_flow, graph)
    ne_times = list(graph.find_path_travel_times(ne_flows, paths_list).values())

    numerator = sum(np.multiply(ne_times, ne_flows))
    denominator = sum(np.multiply(so_times, so_flows))
    poa = numerator / denominator

    return poa


## Function to find cost
def find_cost(origin: int, destination: int, total_flow: int, graph: UndirGraph):

    list_of_paths = graph.list_of_paths(origin, destination)

    NE_path_flows = single_pair_ne.get_NE_flows(origin, destination, total_flow, graph)
    NE_path_travel_times = list(graph.find_path_travel_times(NE_path_flows, list_of_paths).values())

    cost = sum(np.multiply(NE_path_travel_times, NE_path_flows))

    return cost


## Function to calculate all POAs and costs
def find_poas_costs(total_flow: int, cap_adjust: float, edge_adjusted: tuple, graph: UndirGraph, FILENAME: str):
    entries = []

    for pair in itertools.permutations([vertex for vertex in gt.Graph.get_vertices(graph.g)], 2):
        a, b = pair
        od_pair = (a, b)
        list_of_paths = [tuple(path) for path in gt.all_paths(graph.g, a, b)]

        try:
            if len([path for path in gt.all_paths(graph.g, a, b)]) == 1:
                poa = 1.0
            else:
                poa = find_poa(a, b, total_flow, graph)

        except ValueError:
            pass
    
        else:
            cost = find_cost(a, b, total_flow, graph)

            entries.append({'Capacity adjustment': cap_adjust, 'Edge adjusted': edge_adjusted, 'OD pair': od_pair, 'POA': f'{poa}', 'Cost': f'{cost}'})

    columns = ['Capacity adjustment', 'Edge adjusted', 'OD pair', 'POA', 'Cost']

    ## TODO: decide what to do with this file writing stuff
    with open(FILENAME, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writerows(entries)


## Function to calculate all costs
def find_all_costs(total_flow: int, cap_adjust: float, edge_adjusted: tuple, graph: UndirGraph, FILENAME: str):
    entries = []

    for pair in itertools.permutations([vertex for vertex in gt.Graph.get_vertices(graph.g)], 2):
        a, b = pair
        od_pair = (a, b)
    
        cost = find_cost(a, b, total_flow, graph)

        entries.append({'Capacity adjustment': cap_adjust, 'Edge adjusted': edge_adjusted, 'OD pair': od_pair, 'Cost': f'{cost}'})

    columns = ['Capacity adjustment', 'Edge adjusted', 'OD pair', 'Cost']

    ## TODO: decide what to do with this file writing stuff
    with open(FILENAME, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writerows(entries)