from hypothesis import given, strategies as st
from hypothesis.strategies import composite, lists
from random import randint
from typing import List, Tuple

from traffic_simulator.city_map import CityMapLinkedList


def generate_road_ids(size: int, min_value: int, max_value: int) -> List[int]:
    road_ids = set()

    while len(road_ids) < size:
        road_ids.add(randint(min_value, max_value))

    return list(road_ids)


@composite
def roads(draw, min_value=0, max_value=100, min_size=5, max_size=10) -> Tuple[CityMapLinkedList, List[int]]:
    size = randint(min_size,  max_size)
    city_map = CityMapLinkedList()
    road_ids = generate_road_ids(size, min_value, max_value)

    for road_id in road_ids:
        city_map.insert(road_id)

    return city_map, road_ids


@given(roads())
def test_insert_linked_list_roads(roads_with_ids: Tuple[CityMapLinkedList, List[int]]) -> None:
    city_map = roads_with_ids[0]
    road_ids = roads_with_ids[1]
    road_id = 0

    road = city_map.head

    while road:
        assert road.id == road_ids[road_id]
        road = road.next
        road_id += 1



