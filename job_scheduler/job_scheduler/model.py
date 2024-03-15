from dataclasses import dataclass
from networkx import DiGraph
from typing import List, Optional


@dataclass
class Operation:
    id: str
    time: int

    def execute(self) -> None:
        self.time -= 1


@dataclass
class Job:
    id: int
    operations: DiGraph


@dataclass
class Schedule:
    jobs = Optional[List[Job]]


@dataclass
class Machine:
    id: int
    schedule = Schedule


@dataclass
class JobTracker:
    operation_id: int
    job_id: int
    machine_id: int
    idle_time: int
