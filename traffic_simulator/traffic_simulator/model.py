from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


BENEFIT_MATRIX_COLUMNS =  ["source", "destination", "benefit"]


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






