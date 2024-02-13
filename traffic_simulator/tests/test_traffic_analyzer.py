from pandas import DataFrame
from networkx.classes.graph import Graph
from typing import Dict

from traffic_simulator.model import Trip
from traffic_simulator.traffic_analysis import TrafficAnalyzer


def test_calculate_direct_road_benefit(static_city_map: Graph, static_city_trips: Dict[Trip, Trip]) -> None:
    source = 2
    destination = 0
    shrinkage_factor = 0.60
    expect_benefit = 15.20

    actual_benefit = TrafficAnalyzer._calculate_direct_road_benefit(static_city_map,
                                                                    static_city_trips,
                                                                    source,
                                                                    destination,
                                                                    shrinkage_factor)

    assert expect_benefit == actual_benefit


def test_calculate_indirect_road_benefit(static_city_map: Graph, static_city_trips: Dict[Trip, Trip]) -> None:
    neighbor = 0
    source = 1
    destination = 2
    shrinkage_factor = 0.60
    expect_benefit = 22.80

    actual_benefit = TrafficAnalyzer._calculate_indirect_road_benefit(static_city_map,
                                                                      static_city_trips,
                                                                      neighbor,
                                                                      source,
                                                                      destination,
                                                                      shrinkage_factor)

    assert expect_benefit == actual_benefit


def test_get_road_recommendations(static_city_map: Graph, static_city_trips: Dict[Trip, Trip], static_benefit_matrix: DataFrame) -> None:
    source = 2
    destination = 0
    expect_benefit = TrafficAnalyzer.get_benefit(static_benefit_matrix(0), source, destination)["benefit"].iloc[0]

    actual_benefit_matrix = TrafficAnalyzer.get_road_recommendations(static_city_map, static_city_trips)
    actual_benefit = TrafficAnalyzer.get_benefit(actual_benefit_matrix, source, destination)["benefit"].iloc[0]

    assert expect_benefit == actual_benefit


