import networkx as nx
from networkx.classes.graph import Graph
from random import randint
from typing import List, Tuple
from uuid import uuid4


from traffic_simulator.model import ShortestPathAlgo, Trip


class Simulator:
    @staticmethod
    def generate_map(locations=60,
                     connectedness=0.05,
                     seed=1000,
                     min_road_weight=5,
                     max_road_weight=25) -> Graph:

        city_map = Simulator.generate_city_map(locations, connectedness, seed)

        while not Simulator.is_connected(city_map):
            city_map = Simulator.generate_city_map(locations, connectedness, seed)

        for x, y, attr in city_map.edges(data=True):
            attr['uid'] = uuid4()
            attr['weight'] = randint(min_road_weight, max_road_weight)

        return city_map

    @staticmethod
    def generate_trips(city_map: Graph, shortest_path_algo=ShortestPathAlgo.DIJKSTRA, trip_count: int = 100) -> List[Trip]:
        for i in range(0, trip_count):
            start, destination = Simulator.get_random_locations(city_map)
            Simulator.generate_traffic(start, destination, shortest_path_algo)

    @staticmethod
    def generate_traffic(city_map: Graph, start: int, destination: int, shortest_path_algo: ShortestPathAlgo) -> None:

        # TODO Get edge for
        roads = Simulator.get_shortest_path(city_map, start, destination, shortest_path_algo)

        for i in len(roads - 2):
            for

        if not attr['traffic_volume']:
            attr['traffic_volume'] +=
        else:
            attr['traffic_volume'] += 0
    @staticmethod
    def is_connected(city_map: Graph) -> bool:
        return nx.is_connected(city_map)

    @staticmethod
    def generate_city_map(locations: int, connectedness: float, seed: int):
        return nx.gnm_random_graph((locations, connectedness, seed))

    # TODO - Move to traffic analysis for calculating the benefit
    @staticmethod
    def get_shortest_path(city_map: Graph, start: int, destination: int, shortest_path_algo: ShortestPathAlgo) -> List[int]:
        if shortest_path_algo == ShortestPathAlgo.A_STAR.value:
            return nx.astar_path(city_map, start, destination)
        elif shortest_path_algo == ShortestPathAlgo.DIJKSTRA.value:
            return nx.dijkstra_path(city_map, start, destination)

    # TODO - This should get a random adjency node not a random node
    @staticmethod
    def get_random_locations(city_map: Graph) -> Tuple[int, int]:
        number_of_nodes = len(nx.nodes(city_map))

        start = randint(0, number_of_nodes)
        end = randint(0, number_of_nodes)

        while start != end:
            end = randint(0, number_of_nodes)

        return start, end








