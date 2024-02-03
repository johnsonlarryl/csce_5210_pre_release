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
                     max_road_weight=25,
                     shortest_path_algo=ShortestPathAlgo.DIJKSTRA) -> Graph:

        city_map = Simulator.generate_city_map(locations, connectedness, seed)

        while not Simulator.is_connected(city_map):
            city_map = Simulator.generate_city_map(locations, connectedness, seed)

        for x, y, attr in city_map.edges(data=True):
            attr['uid'] = uuid4()
            attr['weight'] = randint(min_road_weight, max_road_weight)

        return city_map

    @staticmethod
    def generate_trips(city_map: Graph, trip_count: int = 100) -> List[Trip]:
        for i in range(0, trip_count):
            # TODO - This should x and y vs. start and end and then get the edge between the two
            start, end = Simulator.get_random_locations(city_map)
            trip_volume = Simulator.get_shortest_path(start, end)

            # TODO Get edge for

            if not attr['traffic_volume']:
                attr['traffic_volume'] += get_shortest_path(x, y)
            else:
             attr['traffic_volume'] += 0

            traffic_volume: int = 0

    @staticmethod
    def is_connected(city_map: Graph) -> bool:
        return nx.is_connected(city_map)

    @staticmethod
    def generate_city_map(locations: int, connectedness: float, seed: int):
        return nx.gnm_random_graph((locations, connectedness, seed))

    # TODO - Move to traffic analysis for calculating the benefit
    @staticmethod
    def get_shortest_path(city_map: Graph, start: int, destination: int, shortest_path_algo: ShortestPathAlgo):
        if shortest_path_algo == ShortestPathAlgo.A_STAR.value:
            return nx.astar_path_length(city_map, start, destination)
        elif shortest_path_algo == ShortestPathAlgo.DIJKSTRA.value:
            return nx.dijkstra_path_length(city_map, start, destination)

    # TODO - This should get a random adjency node not a random node
    @staticmethod
    def get_random_locations(city_map: Graph) -> Tuple[int, int]:
        number_of_nodes = len(nx.nodes(city_map))

        start = randint(0, number_of_nodes)
        end = randint(0, number_of_nodes)

        while start != end:
            end = randint(0, number_of_nodes)

        return start, end








