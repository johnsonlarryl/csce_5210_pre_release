import networkx as nx
from networkx.classes.graph import Graph
from random import randint
from typing import List, Tuple

from traffic_simulator.city_map import CityMap
from traffic_simulator.model import ShortestPathAlgo


class Simulator:
    @staticmethod
    def generate_trips(city_map: Graph, shortest_path_algo=ShortestPathAlgo.DIJKSTRA, trip_count: int = 100) -> None:
        for i in range(0, trip_count):
            source, destination = Simulator.get_random_locations(city_map)
            Simulator.generate_traffic(source, destination, shortest_path_algo)

    @staticmethod
    def generate_traffic(city_map: Graph, source: int, destination: int, shortest_path_algo: ShortestPathAlgo) -> None:
        road_ids = CityMap.get_shortest_path(city_map, source, destination, shortest_path_algo)
        i = 0

        while i < len(road_ids):
            current_location = road_ids[i]
            next_location = road_ids[i]
            metadata = city_map.edges[current_location, next_location]

            if not metadata['traffic_volume']:
                metadata['traffic_volume'] = 0
            else:
                metadata['traffic_volume'] += 1

            i = +1

    @staticmethod
    def get_random_locations(city_map: Graph) -> Tuple[int, int]:
        number_of_nodes = len(nx.nodes(city_map))

        source = randint(0, number_of_nodes - 1)
        destination = randint(0, number_of_nodes - 1)

        while source == destination:
            destination = randint(0, number_of_nodes - 1)

        return source, destination








