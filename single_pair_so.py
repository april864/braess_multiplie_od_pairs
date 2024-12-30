import scipy
from single_pair_graph import UndirGraph
import numpy


## Function to find global mean
# Create function to be optimized
def find_global_mean(path_flows: list, total_flow: int, list_of_paths: list, graph: UndirGraph):

    path_travel_time_dict = graph.find_path_travel_times(path_flows, list_of_paths)

    # Find average travel time across network, weighted by number of cars
    weighted_sum = 0
    
    for path in path_travel_time_dict:
        time = path_travel_time_dict[path]
        index = list(path_travel_time_dict.keys()).index(path)
        weighted_sum += time * path_flows[index]
        
    weighted_average = weighted_sum/total_flow

    return weighted_average


## Function to find socially optimal flow
# Optimize
def find_SO(origin: int, destination: int, total_flow: int, graph: UndirGraph):

    list_of_paths = graph.list_of_paths(origin, destination) # paths between origin and destination nodes
    
    # Define bounds
    bounds = [(0, total_flow) for path in list_of_paths]

    # Define linear constraints
    linear_constraint = scipy.optimize.LinearConstraint(A=[1 for path in list_of_paths], lb=total_flow, ub=total_flow)

    # Define initial guess
    x0 = [total_flow/len(list_of_paths) for n in list_of_paths]

    # print(f"SO args: {total_flow}, {list_of_paths}, {graph}")

    # Optimize
    social_optimum = scipy.optimize.minimize(find_global_mean, x0, args=(total_flow, list_of_paths, graph), 
        method='trust-constr',
        constraints=[linear_constraint],
        bounds=bounds,
    )
    
    # print(f"SO results: {social_optimum}")

    nonint_optimal_path_flows = social_optimum['x']

    return nonint_optimal_path_flows


## Function to find socially optimal integer flow
def find_optimal_int_flows(origin: int, destination: int, total_flow: int, graph: UndirGraph):

    list_of_paths = graph.list_of_paths(origin, destination) # paths between origin and destination nodes  

    path_flows = [round(flow, 0) for flow in list(find_SO(origin, destination, total_flow, graph))]
    global_mean = find_global_mean(path_flows, total_flow, list_of_paths, graph)

    mutable_path_flows = path_flows.copy()
    updated_path_flows = [flow + 1 for flow in mutable_path_flows]

    for index in range(0, len(path_flows)):
        for i in range(0, len(path_flows)):
            if i != index and mutable_path_flows[index] >= 1:
                mutable_path_flows[index] -= 1
                mutable_path_flows[i] = updated_path_flows[i]
                adj_global_mean = find_global_mean(mutable_path_flows, total_flow, list_of_paths, graph)
                if adj_global_mean < global_mean:
                    global_mean = adj_global_mean
                else:
                    mutable_path_flows = path_flows.copy()

    return [int(flow) for flow in mutable_path_flows]    