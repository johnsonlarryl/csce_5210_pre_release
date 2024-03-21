import logging
import random

import matplotlib.pyplot as plt
import networkx as nx
from networkx import DiGraph
from networkx.readwrite import json_graph
import sys
from typing import Any, Dict, List, Set, Tuple

from job_scheduler.model import Job, Link, LINKS, NODES, PARALLEL_MACHINES, Operation, Schedule, ScheduledJob, START_NODE

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.WARNING, format=FORMAT)
logger = logging.getLogger(__name__)


class JobScheduler:
    def __init__(self,
                 scheduled_jobs: ScheduledJob,
                 num_ops_per_machine: int,
                 num_of_machines: int) -> Schedule:

        self.scheduled_jobs = scheduled_jobs
        self.num_of_machines = num_of_machines
        self.num_of_operations_per_machine = num_ops_per_machine
        self._init_job_allocations()
        self.idle_time = 0
        self.starting_machine_id = 0
        self.source_job = START_NODE

    @staticmethod
    def generate_scheduled_jobs(num_of_jobs: int,
                                num_of_operations_per_job: int) -> ScheduledJob:
        scheduled_jobs = []

        for job_id in range(1, num_of_jobs + 2):
            operations = []
            for operation_num in range(1, num_of_operations_per_job + 1):
                Operation(id=1, time=3)
                operations.append(Operation(id=operation_num, time=random.choice(range(5, 51))))

            job = ScheduledJob(job_id=job_id, operations=operations)
            scheduled_jobs.append(job)

        return scheduled_jobs

    def _init_job_allocations(self):
        self.job_allocations = {}

        for scheduled_job in self.scheduled_jobs:
            for operation in scheduled_job.operations:
                if scheduled_job.job_id not in self.job_allocations.keys():
                    self.job_allocations[scheduled_job.job_id] = {}

                self.job_allocations[scheduled_job.job_id][operation.id] = operation.time

    def generate_schedule(self) -> Schedule:
        logging.debug("\nProcessing schedule")
        jobs = []

        for scheduled_job in self.scheduled_jobs:
            jobs.append(Job(id=scheduled_job.job_id, operations=self._schedule_job(scheduled_job)))

        return Schedule(jobs=jobs)

    def _schedule_job(self,
                      scheduled_job: ScheduledJob) -> Dict[str, Any]:
        job = {"directed": True}

        temp_nodes: Set[str] = set()
        links = []
        nodes = []
        j = 0
        operation_job_id = 1
        machine_source: Dict[int, str] = {}
        last_node_processed = None
        operation_ids = [operation_id for operation_id in range(1, len(scheduled_job.operations) + 1)]

        while not self._is_job_fully_executed(scheduled_job.job_id):
            temp_links: Set[Link] = set()

            temp_nodes.add(self.source_job)

            parallel_machines: List[Tuple[str, str]] = []

            for machine in range(1, self.num_of_machines + 1):
                machine_id = self.schedule_machine()

                for operation in range(1, self.num_of_operations_per_machine):
                    operation_id = JobScheduler.get_next_operation(operation_ids)

                    if operation_id == -1:
                        break  # No more operations to process

                    if not self._is_job_fully_executed(scheduled_job.job_id):
                        while self.is_operation_fully_executed(scheduled_job, operation_id):
                            self.remove_operation(scheduled_job, operation_id)

                            operation_id = JobScheduler.get_next_operation(operation_ids)

                            if operation_id == -1:
                                break  # No more operations to process

                        if not self._is_job_fully_executed(scheduled_job.job_id):
                            logging.debug(f"Processing -> machine: {machine_id}, Job: {scheduled_job.job_id}, Operation: {operation_id}, Elapsed time before processing: {self.job_allocations[scheduled_job.job_id][operation_id]}")

                            machine_source[machine_id] = self.source_job
                            node_id = self.get_node_id(scheduled_job.job_id, machine_id, operation_job_id)
                            self.process_operation(scheduled_job,
                                                   machine_id,
                                                   operation_id,
                                                   machine_source,
                                                   temp_nodes,
                                                   temp_links,
                                                   parallel_machines,
                                                   node_id)
                            machine_source[machine_id] = node_id
                            last_node_processed = node_id
                            operation_ids.append(operation_id)
                            operation_job_id += 1

                            logging.debug(f"Parallel Job: {operation} -> {parallel_machines}")
                            logging.debug(f"Temp Link: {temp_links}")
                            logging.debug(f"Processing -> machine: {machine_id}, Job: {scheduled_job.job_id}, Operation: {operation_id}, Elapsed time after processing: {self.job_allocations[scheduled_job.job_id][operation_id]}")

            self.source_job = last_node_processed

            for link in temp_links:
                links.append({"source": link.source,
                              "target": link.target,
                              "weight": link.weight,
                              PARALLEL_MACHINES: parallel_machines})

        for node in temp_nodes:
            nodes.append({"id": node})

        job[NODES] = nodes
        job[LINKS] = links

        return JobScheduler.load_graph(job)

    @staticmethod
    def get_next_operation(operation_ids: List[int]) -> int:
        if len(operation_ids) > 0:
            return operation_ids.pop(0)
        else:
            return -1  # No more operations to process

    def remove_operation(self, scheduled_job:ScheduledJob, operation_id: int) -> None:
        if operation_id in self.job_allocations[scheduled_job.job_id].keys():
            del self.job_allocations[scheduled_job.job_id][operation_id]

    def is_operation_fully_executed(self, scheduled_job: ScheduledJob, operation_id: int) -> bool:
        return operation_id not in self.job_allocations[scheduled_job.job_id].keys() or \
               self.job_allocations[scheduled_job.job_id][operation_id] < 1

    def schedule_machine(self) -> int:
        self.starting_machine_id += 1

        if self.starting_machine_id > self.num_of_machines:
            self.starting_machine_id = 1

        return self.starting_machine_id

    def process_operation(self,
                          scheduled_job: ScheduledJob,
                          machine_id: int,
                          operation_id: int,
                          machine_source: Dict[int, str],
                          temp_nodes: Set[str],
                          temp_links: Set[Link],
                          parallel_machines: List[Tuple[str, str]],
                          node_id: int) -> None:
        time = min(self.num_of_operations_per_machine, self.job_allocations[scheduled_job.job_id][operation_id])
        self.idle_time += self.num_of_operations_per_machine - self.job_allocations[scheduled_job.job_id][operation_id]
        temp_nodes.add(node_id)
        link = Link(source=machine_source[machine_id],
                    target=node_id,
                    weight=time)
        temp_links.add(link)
        parallel_machines.append((machine_source[machine_id], node_id))
        self.job_allocations[scheduled_job.job_id][operation_id] -= time

        machine_source[machine_id] = node_id

    def get_node_id(self, job_id: int, machine_id: int, operation_id: int) -> str:
        return f"J{job_id}{machine_id}{operation_id}"

    def _is_job_fully_executed(self, job_id):
        time = 0

        for operation_id in self.job_allocations[job_id].keys():
            time += self.job_allocations[job_id][operation_id]

        return time < 1

    @staticmethod
    def load_graph(schedule: str):
        return json_graph.node_link_graph(schedule, directed=True)

    @staticmethod
    def visualize_schedule(job: DiGraph, fig_size: Tuple = (12, 8)) -> None:

        pos = nx.nx_agraph.graphviz_layout(job, prog='dot')
        plt.figure(figsize=fig_size)

        nx.draw(job, pos, with_labels=True, node_size=600, node_color="lightblue", font_size=10, arrows=True)

        edge_labels = dict(((source_operation, destination_operation), machine['weight']) for source_operation, destination_operation, machine in job.edges(data=True))

        for (source_operation, destination_operation), weight in edge_labels.items():
            label = f"{weight}"
            x, y = pos[source_operation]
            dx, dy = pos[destination_operation]
            plt.text(x * 0.5 + dx * 0.5, y * 0.5 + dy * 0.5,
                     label,
                     horizontalalignment='center',
                     verticalalignment='center',
                     bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

        plt.show()
















