from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ShortestPathAlgo(Enum):
    A_STAR = "astar"
    DIJKSTRA = "dijkstra"


@dataclass
class Road(object):
    id: int
    next: Optional[object] = None






