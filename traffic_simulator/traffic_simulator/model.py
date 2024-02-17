from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


BENEFIT_MATRIX_COLUMNS = ["source", "destination", "benefit"]

BENEFIT_MATRIX_TRUTH_TABLE_COLUMNS = ["x",
                                      "y",
                                      "nx_neighbor",
                                      "ny_neighbor",
                                      "nx_indirect_benefits",
                                      "ny_indirect_benefits",
                                      "indirect_x",
                                      "indirect_y",
                                      "has_edge_indirect_x_y",
                                      "has_edge_nx_neighbor_indirect_y",
                                      "has_edge_indirect_x_x",
                                      "has_edge_ny_neighbor_indirect_y"]


class ShortestPathAlgo(Enum):
    A_STAR = "astar"
    DIJKSTRA = "dijkstra"


@dataclass
class Road:
    metadata: Dict
    next: Optional[object] = None


@dataclass
class Trip:
    source: int
    destination: int
    numer_of_trips: Optional[int] = 0

    def __hash__(self):
        return hash((self.source, self.destination))

    def __eq__(self, other):
        return self.source == other.source and \
               self.destination == other.destination


class TripFactory:
    @staticmethod
    def create_trip(source: int,
                    destination: int,
                    numer_of_trips: int = 0):
        return Trip(source, destination, numer_of_trips)


class TimeDeltaDiff(Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    MONTHS = "months"
    YEARS = "years"




