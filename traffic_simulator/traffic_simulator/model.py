from dataclasses import dataclass
from enum import Enum
from networkx as nx
from uuid import uuid4

class ShortestPathAlgo(Enum):
    A_STAR = "astar"
    DIJKSTRA = "dijkstra"


@dataclass(frozen=True)
class Object:
    @property
    def uid(self):
        return uuid4()


@dataclass(frozen=True)
class Location(Object):
    name: str


@dataclass(frozen=True)
class Trip(Object):
    start: Location
    end: Location
    distance: int = 0

    def __post_init__(self):
        if self.distance <= 0:
            raise TypeError(f'Trip distance (length) has to greater than 0 km.')


@dataclass
class Road:
    uid: int
    benefit: float


    def __post_init__(self):
        if self.traffic_volume <= 0:
            raise TypeError(f'Traffic volume has to be greater than 0 trips.')



