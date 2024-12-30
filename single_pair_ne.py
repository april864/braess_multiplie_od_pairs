import graph_tool.all as gt
import single_pair_so
from single_pair_graph import UndirGraph


## Helper function to move one driver to a shorter path
def moveDriver(list_of_paths: list, path_flows: list, graph: UndirGraph):

    travel_times = list(graph.find_path_travel_times(path_flows, list_of_paths).values()) # use socially optimal travel times

    # find slowest time at social optimum
    slowest_time = 0
    for time in travel_times:
        if path_flows[travel_times.index(time)] >= 1 and time > slowest_time:
            slowest_time = time

    path_flows[travel_times.index(slowest_time)] -= 1 # remove one driver from path with slowest travel time

    # move one driver from slowest path to a faster path
    for i in range(0, len(path_flows)): # for each element in path_flows list

        path_flows[i] += 1 # move the driver to new path
        new_travel_times = list(graph.find_path_travel_times(path_flows, list_of_paths).values()) # calculate new travel times

        if new_travel_times[i] < slowest_time: # if the driver has moved to a faster path:
            travel_times = new_travel_times
            return path_flows # return updated path flows
        else:
            path_flows[i] -= 1

    # if we've reached here, the driver will stay on their original path
    path_flows[travel_times.index(slowest_time)] += 1 
    return path_flows # return unchanged path flows


## Function to find Nash equilibrium flow over network
def get_NE_flows(origin: int, destination: int, total_flow: int, graph: UndirGraph):

    list_of_paths = graph.list_of_paths(origin, destination) # paths between origin and destination nodes
    path_flows = single_pair_so.find_optimal_int_flows(origin, destination, total_flow, graph) # socially optimal flow across each path

    prev = path_flows
    cur = moveDriver(list_of_paths, path_flows, graph)
    while prev != cur:
        prev = cur
        cur = moveDriver(list_of_paths, path_flows, graph)
        # if moveDriver(list_of_paths, path_flows, graph) == "done":
        #     break

    return cur