from networkx.classes.graph import Graph
from pandas import DataFrame
from typing import Dict, List, Set, Tuple

from traffic_simulator.city_map import CityMap
from traffic_simulator.model import BENEFIT_MATRIX_COLUMNS, Trip, TripFactory


class TrafficAnalyzer:
    @staticmethod
    def get_road_recommendations(city_map: Graph,
                                 trips: Dict[Trip, Trip],
                                 shrinkage_factor=0.6) -> DataFrame:
        """
        Generates benefit matrix based on the city map or graph and the list of trips across each road segment
        The result of the matrix should look something like the following:
        src(x)      dst(y)      benefit(b)
        0           2           38.00
        0           3           12.80
        ...         ...         ...
        2           3           38.60

        Parameters:
        city_map:   Network Graph representation of the city map
        trips:      Dictionary representation of each trip across a particular road segment

        Returns:
        benefit_matrix: Matrix representation of the benefit matrix showing each calculated road benefit
        """
        road_candidates = CityMap.get_new_road_candidates(city_map)
        benefit_matrix_data = []

        for candidate in road_candidates:
            x = candidate[0]
            y = candidate[1]
            n1 = set(city_map.neighbors(y))
            n2 = set(city_map.neighbors(x))

            nx_indirect_benefits = set()
            ny_indirect_benefits = set()

            TrafficAnalyzer._calculate_all_road_benefits(city_map,
                                                         trips,
                                                         benefit_matrix_data,
                                                         shrinkage_factor,
                                                         x,
                                                         y,
                                                         n1,
                                                         n2,
                                                         nx_indirect_benefits,
                                                         ny_indirect_benefits)

        benefit_matrix_data = DataFrame(benefit_matrix_data, columns=BENEFIT_MATRIX_COLUMNS)

        return benefit_matrix_data.sort_values(by='benefit', ascending=False)

    @staticmethod
    def _calculate_all_road_benefits(city_map: Graph,
                                     trips: Dict[Trip, Trip],
                                     benefit_matrix_data: List[Tuple[int, int, float]],
                                     shrinkage_factor,
                                     x: int,
                                     y: int,
                                     n1: Set[int],
                                     n2: Set[int],
                                     nx_indirect_benefits: Set,
                                     ny_indirect_benefits: Set) -> None:
        indirect_road_benefits = 0

        direct_road_benefits = TrafficAnalyzer._calculate_direct_road_benefit(city_map,
                                                                              trips,
                                                                              x,
                                                                              y,
                                                                              shrinkage_factor)

        for nx_neighbor in n1:
            nx_indirect_benefits = nx_indirect_benefits.union(TrafficAnalyzer._get_indirect_benefit(city_map,
                                                                                                    x,
                                                                                                    nx_neighbor))

            for nx_indirect_benefit in nx_indirect_benefits:
                indirect_x = nx_indirect_benefit[0]
                indirect_y = nx_indirect_benefit[1]

                if city_map.has_edge(indirect_x, y) and city_map.has_edge(nx_neighbor, indirect_y):
                    indirect_road_benefits += TrafficAnalyzer._calculate_indirect_road_benefit(city_map,
                                                                                               trips,
                                                                                               y,
                                                                                               indirect_x,
                                                                                               indirect_y,
                                                                                               shrinkage_factor)

        for ny_neighbor in n2:
            ny_indirect_benefits = ny_indirect_benefits.union(TrafficAnalyzer._get_indirect_benefit(city_map,
                                                                                                    y,
                                                                                                    ny_neighbor))

            for ny_indirect_benefit in ny_indirect_benefits:
                indirect_x = ny_indirect_benefit[0]
                indirect_y = ny_indirect_benefit[1]

                if city_map.has_edge(indirect_x, x) and city_map.has_edge(ny_neighbor, indirect_y):
                    indirect_road_benefits += TrafficAnalyzer._calculate_indirect_road_benefit(city_map,
                                                                                               trips,
                                                                                               x,
                                                                                               indirect_x,
                                                                                               indirect_y,
                                                                                               shrinkage_factor)

        b = direct_road_benefits + indirect_road_benefits

        benefit_matrix_data.append((x, y, b))

    @staticmethod
    def _get_indirect_benefit(city_map, source, destination):
        indirect_benefits = set()

        if not city_map.has_edge(source, destination):
            indirect_benefits.add((source, destination))
            indirect_benefits.add((destination, source))

        return indirect_benefits

    @staticmethod
    def _calculate_direct_road_benefit(city_map: Graph,
                                       trips: Dict[Trip, Trip],
                                       source: int,
                                       destination: int,
                                       shrinkage_factor: float) -> float:
        source_to_destination_trips = trips[TripFactory.create_trip(source, destination)].numer_of_trips
        destination_to_source_trips = trips[TripFactory.create_trip(destination, source)].numer_of_trips

        shortest_path = CityMap.get_shortest_path_length(city_map, source, destination)

        return (shortest_path - (shortest_path * shrinkage_factor)) * \
            (source_to_destination_trips + destination_to_source_trips)

    @staticmethod
    def _calculate_indirect_road_benefit(city_map: Graph,
                                         trips: Dict[Trip, Trip],
                                         neighbor: int,
                                         source: int,
                                         destination: int,
                                         shrinkage_factor: float):

        source_to_destination_trips = trips[TripFactory.create_trip(source, destination)].numer_of_trips
        destination_to_source_trips = trips[TripFactory.create_trip(destination, source)].numer_of_trips

        existing_road_shortest_path = CityMap.get_shortest_path_length(city_map, neighbor, destination)
        new_road_shortest_path = CityMap.get_shortest_path_length(city_map, source, destination)
        neighbor_shortest_path = CityMap.get_shortest_path_length(city_map, neighbor, source)

        return round(max((new_road_shortest_path -
                          (existing_road_shortest_path * shrinkage_factor + neighbor_shortest_path)), 0) *
                     (source_to_destination_trips + destination_to_source_trips), 5)

    @staticmethod
    def get_benefit(benefit_matrix: DataFrame,
                    source: int,
                    destination: int):
        return benefit_matrix[((benefit_matrix["source"] == source) & (benefit_matrix["destination"] == destination)) |
                              ((benefit_matrix["source"] == destination) & (benefit_matrix["destination"] == source))]

    @staticmethod
    def get_max_road_benefit(benefit_matrix: DataFrame) -> DataFrame:
        max_road_benefit = benefit_matrix[BENEFIT_MATRIX_COLUMNS[2]].idxmax()
        return benefit_matrix.loc[[max_road_benefit]]
