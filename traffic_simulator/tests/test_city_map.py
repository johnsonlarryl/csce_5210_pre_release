from hypothesis import given
from hypothesis.strategies import composite
from random import randint
from typing import List, Tuple

from traffic_simulator.city_map import TripLinkedList
from traffic_simulator.model import Trip, TripFactory


def generate_road_ids(size: int, min_value: int, max_value: int) -> List[int]:
    road_ids = set()

    while len(road_ids) < size:
        road_ids.add(randint(min_value, max_value))

    return list(road_ids)


@composite
def roads(draw, min_value=0, max_value=100, min_size=5, max_size=10) -> Tuple[TripLinkedList, List[int]]:
    size = randint(min_size,  max_size)
    trip = TripLinkedList()
    road_ids = generate_road_ids(size, min_value, max_value)

    for road_id in road_ids:
        trip.insert({"id": road_id})

    return trip, road_ids


@given(roads())
def test_insert_linked_list_roads(roads_with_ids: Tuple[TripLinkedList, List[int]]) -> None:
    trip = roads_with_ids[0]
    road_ids = roads_with_ids[1]
    road_id = 0

    next_road = trip.head

    while next_road:
        assert next_road.metadata["id"] == road_ids[road_id]
        next_road = next_road.next
        road_id += 1


def test_trip_equality_equal():
    trip_a = TripFactory.create_trip(0, 2, 1)
    trip_b = TripFactory.create_trip(0, 2, 10)

    assert trip_a == trip_b


def test_trip_equality_not_equal():
    trip_a = TripFactory.create_trip(0, 2, 1)
    trip_b = TripFactory.create_trip(2, 0, 11)

    assert trip_a != trip_b
