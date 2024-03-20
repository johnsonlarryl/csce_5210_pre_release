from dataclasses import dataclass
from networkx import DiGraph
from typing import List, Optional, Tuple

PARALLEL_MACHINES = 'parallel_machines'
NODES = "nodes"
LINKS = "links"
START_NODE = "start"


@dataclass
class Operation:
    id: int
    time: int


@dataclass
class Job:
    id: int
    operations: DiGraph


@dataclass
class Schedule:
    jobs: Optional[List[Job]]
    debug: bool = False

    def compute_makespan(self) -> int:
        make_span = 0

        for job in self.jobs:
            operations = job.operations
            nodes_counted: Tuple[str, str] = []

            for source_operation, destination_operation, machine in operations.edges(data=True):
                if PARALLEL_MACHINES in machine.keys():
                    max_ops_time = Schedule.get_max_ops_time(operations, machine[PARALLEL_MACHINES], nodes_counted)

                    if self.debug:
                        print(f"Source: {source_operation} \
                               Destination: {destination_operation} \
                               Machine Operations: {machine['parallel_machines']} \
                               Max_Ops_Time: {max_ops_time}")

                    make_span += max_ops_time

        return make_span

    @staticmethod
    def get_max_ops_time(operations: DiGraph,
                         parallel_machines: List[Tuple[str, str]],
                         nodes_counted: Tuple[str, str]):
        ops_times = []

        for parallel_op in parallel_machines:
            if parallel_op not in nodes_counted:
                operation = operations.get_edge_data(parallel_op[0], parallel_op[1])
                nodes_counted.append(parallel_op)
                ops_times.append(operation[0]['weight'])

        if len(ops_times) > 0:
            return max(ops_times)
        else:
            return 0


@dataclass
class Machine:
    id: int
    schedule = Schedule


@dataclass
class ScheduledJob:
    job_id: int
    operations: List[Operation]


@dataclass(frozen=True)
class Link:
    source: str
    target: str
    weight: int

