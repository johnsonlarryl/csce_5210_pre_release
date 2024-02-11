from itertools import permutations
import networkx as nx
from networkx.classes.graph import Graph
from random import randint
from typing import Any, Dict, List, Set, Tuple
from uuid import uuid4


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
    def generate_map(locations=60,
                     connectedness=0.05,
                     seed=1000,
                     min_road_weight=5,
                     max_road_weight=25) -> Graph:

        city_map = CityMap.generate_city_map(locations, connectedness, seed)

        while not CityMap.is_connected(city_map):
            city_map = CityMap.generate_city_map(locations, connectedness, seed)

        for x, y, attr in city_map.edges(data=True):
            attr['uid'] = uuid4()
            attr['weight'] = randint(min_road_weight, max_road_weight)

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
    def generate_city_map(locations: int, connectedness: float, seed: int):
        return nx.gnm_random_graph((locations, connectedness, seed))

    @staticmethod
    def is_connected(city_map: Graph) -> bool:
        return nx.is_connected(city_map)

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
