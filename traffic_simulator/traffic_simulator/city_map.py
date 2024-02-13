
from itertools import permutations
import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes.graph import Graph
from typing import Any, Dict, List, Set, Tuple


from traffic_simulator.model import Road, ShortestPathAlgo


class TripLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, metadata: Dict) -> None:
        new_road = Road(metadata=metadata)

        if self.head is None:
            self.head = new_road
            return

        current_road = self.head

        while current_road.next:
            current_road = current_road.next

        current_road.next = new_road


class CityMap:
    @staticmethod
    def get_road_permutations(city_map: Graph,
                              source: int,
                              destination: int, shortest_path_algo: ShortestPathAlgo) -> List[Tuple[int, int]]:
        if shortest_path_algo == ShortestPathAlgo.A_STAR.value:
            shortest_path = nx.astar_path(city_map, source, destination)
        elif shortest_path_algo == ShortestPathAlgo.DIJKSTRA.value:
            shortest_path = nx.dijkstra_path(city_map, source, destination)

        return list(permutations(shortest_path))

    @staticmethod
    def get_possible_trips(city_map: Graph) -> Set[Tuple[int, int]]:
        locations = list(city_map.nodes())

        trips = set()

        for source, destination in permutations(locations, 2):
            trips.add((source, destination))

        return trips

    @staticmethod
    def get_existing_roads(city_map: Graph) -> Set[Tuple[int, int]]:
        return set(nx.edges(city_map))

    @staticmethod
    def get_new_road_candidates(city_map: Graph):
        return set(nx.non_edges(city_map))

    @staticmethod
    def get_road_segment(city_map: Graph, source: int, destination: int) -> Dict[str, Any]:
        return city_map.get_edge_data(source, destination)

    @staticmethod
    def get_shortest_path(city_map: Graph, source: int, destination: int, shortest_path_algo=ShortestPathAlgo.DIJKSTRA) -> List[int]:
        if shortest_path_algo == ShortestPathAlgo.A_STAR:
            return nx.astar_path(city_map, source, destination)
        elif shortest_path_algo == ShortestPathAlgo.DIJKSTRA:
            return nx.dijkstra_path(city_map, source, destination)

    @staticmethod
    def get_shortest_path_length(city_map: Graph, source: int, destination: int, shortest_path_algo=ShortestPathAlgo.DIJKSTRA) -> List[int]:
        if shortest_path_algo == ShortestPathAlgo.A_STAR:
            return nx.astar_path_length(city_map, source, destination)
        elif shortest_path_algo == ShortestPathAlgo.DIJKSTRA:
            return nx.dijkstra_path_length(city_map, source, destination)

    @staticmethod
    def add_road_segment(city_map: Graph, source: int, destination: int, shrinkage_factor=0.6, shortest_path_algo=ShortestPathAlgo.DIJKSTRA) -> None:
        road_length = nx.astar_path_length(city_map, source, destination) * shrinkage_factor
        city_map.add_edge(source, destination, weight=road_length)

    @staticmethod
    def get_city_map_statistics(city_map: Graph) ->None:
        print("node degree and node clustering")
        for v in nx.nodes(city_map):
            print(f"{v} {nx.degree(city_map, v)} {nx.clustering(city_map, v)}")

        print()
        print("the adjacency list")
        for line in nx.generate_adjlist(city_map):
            print(line)

    @staticmethod
    def visualize_city_map(city_map: Graph, location_size=1200, location_font_size=20, road_widths=4) -> None:
        links = [(u, v) for (u, v, d) in city_map.edges(data=True)]
        pos = nx.nx_pydot.graphviz_layout(city_map)
        nx.draw_networkx_nodes(city_map, pos, node_size=location_size, node_color='lightblue', linewidths=0.25)  # draw nodes
        nx.draw_networkx_edges(city_map, pos, edgelist=links, width=road_widths)  # draw edges

        # node labels
        nx.draw_networkx_labels(city_map, pos, font_size=location_font_size, font_family="sans-serif")

        # edge weight labels
        edge_labels = nx.get_edge_attributes(city_map, 'weight', 'trips')
        print(edge_labels)
        nx.draw_networkx_edge_labels(city_map, pos, edge_labels)

        plt.show()

