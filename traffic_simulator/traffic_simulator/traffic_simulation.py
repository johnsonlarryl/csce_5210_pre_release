from datetime import datetime
from dateutil.relativedelta import relativedelta
import networkx as nx
from networkx.classes.graph import Graph
from random import randint
from typing import Dict, Tuple


from traffic_simulator.city_map import CityMap
from traffic_simulator.model import ShortestPathAlgo, TimeDeltaDiff, Trip, TripFactory


class Simulator:
    @staticmethod
    def generate_map(locations=60,
                     connectedness=0.05,
                     step_connectedness=0.01,
                     seed=1000,
                     min_road_weight=5,
                     max_road_weight=25) -> Graph:

        city_map = Simulator.generate_city_map(locations, connectedness, seed)

        while not Simulator.is_connected(city_map):
            connectedness += step_connectedness
            city_map = Simulator.generate_city_map(locations, connectedness, seed)

        for x, y, attr in city_map.edges(data=True):
            attr['weight'] = randint(min_road_weight, max_road_weight)

        return city_map

    @staticmethod
    def generate_trips(city_map: Graph,
                       traffic_start_date: datetime,
                       traffic_end_date: datetime,
                       traffic_time_delta_difference: TimeDeltaDiff
                       ) -> Dict[Trip, Trip]:
        trips = {}

        for _ in range(Simulator.get_number_trips_to_generate(traffic_start_date,
                                                        traffic_end_date,
                                                        traffic_time_delta_difference)):
            source, destination = Simulator.get_random_locations(city_map)
            trip = TripFactory.create_trip(source, destination)

            if trip not in trips:
                trips[trip] = trip

            trips[trip].numer_of_trips += 1

        return trips

    @staticmethod
    def generate_city_map(locations: int, connectedness: float, seed: int):
        return nx.gnm_random_graph(locations, connectedness, seed)

    @staticmethod
    def is_connected(city_map: Graph) -> bool:
        return nx.is_connected(city_map)

    @staticmethod
    def get_number_trips_to_generate(traffic_start_date: datetime,
                                     traffic_end_date: datetime,
                                     traffic_time_delta_difference):
        difference = relativedelta(traffic_end_date, traffic_start_date)

        if traffic_time_delta_difference == TimeDeltaDiff.SECONDS:
            return int((traffic_end_date - traffic_start_date).total_seconds())
        elif traffic_time_delta_difference == TimeDeltaDiff.MINUTES:
            return int(difference.minutes)
        elif traffic_time_delta_difference == TimeDeltaDiff.HOURS:
            return int(difference.hours)
        elif traffic_time_delta_difference == TimeDeltaDiff.DAYS:
            return int(difference.days)
        elif traffic_time_delta_difference == TimeDeltaDiff.DAYS:
            return int(relativedelta(traffic_start_date - traffic_end_date).months)
        elif traffic_time_delta_difference == TimeDeltaDiff.YEARS:
            return int(difference.years)

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








