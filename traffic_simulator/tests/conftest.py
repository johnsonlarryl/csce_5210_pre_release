import networkx as nx
from pandas import DataFrame
from networkx.classes.graph import Graph
import pytest
from typing import Dict

from traffic_simulator.city_map import CityMap
from traffic_simulator.model import BENEFIT_MATRIX_COLUMNS, Trip, TripFactory


def generate_static_city_map() -> Graph:
    graph = nx.Graph()

    graph.add_edges_from([
        (0, 1, {'weight': 6}),
        (0, 4, {'weight': 9}),
        (1, 3, {'weight': 11}),
        (2, 4, {'weight': 10}),
        (3, 4, {'weight': 7}),
    ])

    return graph


@pytest.fixture
def static_city_map() -> Graph:
    return generate_static_city_map()


def generate_static_trips() -> Dict[Trip, Trip]:
    trip_a = TripFactory.create_trip(0, 2, 1)
    trip_b = TripFactory.create_trip(2, 0, 1)
    trip_c = TripFactory.create_trip(0, 3, 1)
    trip_d = TripFactory.create_trip(3, 0, 1)
    trip_e = TripFactory.create_trip(1, 2, 1)
    trip_f = TripFactory.create_trip(2, 1, 2)
    trip_g = TripFactory.create_trip(1, 4, 1)
    trip_h = TripFactory.create_trip(4, 1, 2)
    trip_i = TripFactory.create_trip(2, 3, 3)
    trip_j = TripFactory.create_trip(3, 2, 1)

    trips = {trip_a: trip_a,
             trip_b: trip_b,
             trip_c: trip_c,
             trip_d: trip_d,
             trip_e: trip_e,
             trip_f: trip_f,
             trip_g: trip_g,
             trip_h: trip_h,
             trip_i: trip_i,
             trip_j: trip_j}

    city_map = generate_static_city_map()
    possible_trips = CityMap.get_possible_trips(city_map)

    for possible_trip in possible_trips:
        source = possible_trip[0]
        destination = possible_trip[1]
        trip = TripFactory.create_trip(source, destination)

        if trip not in trips.keys():
            trips[trip] = trip

    return trips


@pytest.fixture
def static_city_trips() -> Dict[Trip, Trip]:
    return generate_static_trips()


@pytest.fixture
def static_benefit_matrix() -> DataFrame:
    def get_benefit_matrix(k: int) -> DataFrame:
        if k == 0:
            benefit_matrix_data = [
                [0, 2, 38.00]
            ]
            return DataFrame(benefit_matrix_data, columns=BENEFIT_MATRIX_COLUMNS)

    return get_benefit_matrix










