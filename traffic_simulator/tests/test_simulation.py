from itertools import permutations
from typing import List

from traffic_simulator.traffic_simulation import Simulator


def test_get_random_locations(static_city_map) -> None:
    source, destination = Simulator.get_random_locations(static_city_map)

    assert (isinstance(source, int) and isinstance(destination, int))
    assert (source != destination)


def test_get_shortest_dijkstra_path(static_city_map) -> None:
    pass


def test_get_shortest_astar_path(static_city_map) -> None:
    pass
