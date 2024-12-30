import graph_tool.all as gt
import numpy as np


## Class of "undirected" graph
class UndirGraph:

    ## Constructor (make graph)
    def __init__(self):
        # for random graph later, inlude num_vertices (6) and edge_prob (0.5)
        self.g = gt.Graph()

        ## Braess paradox graph---broken?
        # self.e1 = self.g.add_edge(0, 1) 
        # self.e2 = self.g.add_edge(1, 2)
        # self.e3 = self.g.add_edge(0, 3)
        # self.e4 = self.g.add_edge(3, 2)
        # self.e5 = self.g.add_edge(1, 3)

        self.e1 = self.g.add_edge(0, 1) 
        self.e2 = self.g.add_edge(0, 3)
        self.e3 = self.g.add_edge(0, 5)
        self.e4 = self.g.add_edge(1, 0)
        self.e5 = self.g.add_edge(1, 2)
        self.e6 = self.g.add_edge(1, 3)
        self.e7 = self.g.add_edge(2, 1)
        self.e8 = self.g.add_edge(2, 4)
        self.e9 = self.g.add_edge(2, 5)
        self.e10 = self.g.add_edge(3, 0)
        self.e11 = self.g.add_edge(3, 1)
        self.e12 = self.g.add_edge(3, 4)
        self.e13 = self.g.add_edge(3, 5)
        self.e14 = self.g.add_edge(4, 2)
        self.e15 = self.g.add_edge(4, 3)
        self.e16 = self.g.add_edge(5, 0)
        self.e17 = self.g.add_edge(5, 2)
        self.e18 = self.g.add_edge(5, 3)

        self.pos = gt.sfdp_layout(self.g, cooling_step=0.95, epsilon=1e-2)

        # Capacity: cars/time
        self.capacity = self.g.new_edge_property("double")                
        for e in self.g.edges():
            self.capacity[e] = 2000
            # self.capacity[e] = np.random.normal(loc=2000, scale=1000)

        # Length: length
        self.length = self.g.new_edge_property("double")                
        for e in self.g.edges():
            self.length[e] = 10.0 

        # Speed limit: length/time
        self.speed_limit = self.g.new_edge_property("double")       
        for e in self.g.edges():         
            self.speed_limit[e] = 45.0

    
    ##
    ## draw()
    ##
    ## Draws the graph to a separate file
    ##
    def draw(self, image_output: str):
        edge_label = self.g.new_edge_property("string")    
        for e in self.g.edges():
            edge_label[e] = f"Cap.:{self.capacity[e]}; Len.: {self.length[e]}; Speed limit: {self.speed_limit[e]}"

        gt.graph_draw(
            self.g, 
            pos=self.pos,
            output_size=(1000, 1000),
            edge_color="gray",
            vertex_size=40,
            vertex_text=self.g.vertex_index, 
            edge_text=edge_label,
            edge_font_size=10,
            edge_text_color="white",
            edge_text_distance=10,
            output=image_output
            )
        
    
    ##
    ## get_edges()
    ##
    ## Returns edges of graph
    ##
    def get_edges(self):
        g = self.g
        return g.get_edges()

    ##
    ## list_of_paths()
    ##
    ## Given a source node and target node, returns a list of paths between those two nodes
    ##
    def list_of_paths(self, source: int, target: int):
        list_of_paths = [tuple(path) for path in gt.all_paths(self.g, source, target)]
        return list_of_paths


    ##
    ## find_path_travel_times()
    ##
    ## Given a list of path flows, list of paths, and a graph, outputs a dictionary of path travel times by finding 
    ## travel times across each edge of the graph and then summing them to get travel times across each path.
    ##
    def find_path_travel_times(self, path_flows: list, list_of_paths: list):
        path_flow_dict = {item[0]:item[1] for item in zip(list_of_paths, path_flows)}
        # print(path_flow_dict)

        # Flow across each edge:
        flow = self.g.new_edge_property("double")
        for path in list_of_paths:
            edges = [[path[i], path[i + 1]] for i in range(len(path) - 1)]
            for edge in edges:
                flow[self.g.edge(edge[0], edge[1])] += path_flow_dict[path]

        # Travel time across each edge
        a = 0.15
        b = 4
        travel_time = self.g.new_edge_property("double")
        for e in self.g.get_edges():
            u, v = e
            travel_time[self.g.edge(u, v)] = (self.length[self.g.edge(u, v)]/self.speed_limit[self.g.edge(u, v)])*(1+a*(flow[self.g.edge(u, v)]/self.capacity[self.g.edge(u, v)])**b)

        # Travel time across each path
        list_of_path_travel_times = []
        for path in list_of_paths:
            edges = [[path[i], path[i + 1]] for i in range(len(path) - 1)]
            travel_times = [travel_time[self.g.edge(edge[0], edge[1])] for edge in edges]
            path_travel_time = sum(travel_times)
            list_of_path_travel_times.append(path_travel_time)

        path_travel_time_dict = {item[0]:item[1] for item in zip(list_of_paths, list_of_path_travel_times)}
        
        return path_travel_time_dict