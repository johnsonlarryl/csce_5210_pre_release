import matplotlib.pyplot as plt
import networkx as nx
from networkx import DiGraph
from networkx.readwrite import json_graph
from typing import Any, Dict, List, Set, Tuple

from job_scheduler.model import Job, Link, LINKS, NODES, PARALLEL_MACHINES, Schedule, ScheduledJob, START_NODE


class JobScheduler:
    def __init__(self,
                 scheduled_jobs: ScheduledJob,
                 num_ops_per_machine: int,
                 num_of_machines: int,
                 num_of_jobs: int = 0,
                 num_of_operations_per_job: int = 0) -> Schedule:
        if scheduled_jobs:
            self.scheduled_jobs = scheduled_jobs
        else:
            self.num_of_jobs = num_of_jobs
            # TODO - generate scheduled_jobs using
            # num_of_jobs and num_of_operations_per_job and

        self.num_of_machines = num_of_machines
        self.num_of_operations_per_machine = num_ops_per_machine
        self._init_job_allocations()
        self.idle_time = 0
        self.starting_machine_id = 1
        self.source_job = START_NODE

    def _init_job_allocations(self):
        self.job_allocations = {}

        for scheduled_job in self.scheduled_jobs:
            for operation in scheduled_job.operations:
                if scheduled_job.job_id not in self.job_allocations.keys():
                    self.job_allocations[scheduled_job.job_id] = {}

                self.job_allocations[scheduled_job.job_id][operation.id] = operation.time

    def generate_schedule(self) -> Schedule:
        jobs = []

        for scheduled_job in self.scheduled_jobs:
            machines = self.schedule_machines()
            jobs.append(Job(id=scheduled_job.job_id, operations=self._schedule_job(scheduled_job, machines)))

        return Schedule(jobs=jobs)

    def _schedule_job(self,
                      scheduled_job: ScheduledJob,
                      machines: List[int]) -> Dict[str, Any]:
        job = {"directed": True}

        temp_nodes: Set[str] = set()
        links = []
        nodes = []
        j = 0
        operation_job_id = 1
        machine_source: Dict[int, str] = {}

        while not self._is_fully_executed(scheduled_job.job_id):
            temp_links: Set[Link] = set()

            temp_nodes.add(self.source_job)

            for machine_id in machines:
                machine_source[machine_id] = self.source_job

            parallel_machines: List[Tuple[str, str]] = []

            for machine_id in machines:
                if self._is_fully_executed(scheduled_job.job_id):
                    self.starting_machine_id = machine_id
                    break
                else:
                    operation_id = j+1

                    if self.job_allocations[scheduled_job.job_id][operation_id] > 0:
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
                        self.source_job = node_id
                        operation_job_id += 1
                    else:
                        if operation_id == len(self.job_allocations[scheduled_job.job_id].keys()):
                            j = 0
                        else:
                            j += 1

                        continue

                    if operation_id == len(self.job_allocations[scheduled_job.job_id].keys()):
                        j = 0
                    else:
                        j += 1

            for link in temp_links:
                links.append({"source": link.source,
                              "target": link.target,
                              "weight": link.weight,
                              PARALLEL_MACHINES: parallel_machines})

        for node in temp_nodes:
            nodes.append({"id": node})

        job[NODES] = nodes
        job[LINKS] = links

        return job

    def schedule_machines(self) -> List[int]:
        machines = []

        while len(machines) < self.num_of_machines:
            machines.append(self.starting_machine_id)
            self.starting_machine_id += 1

            if self.starting_machine_id > self.num_of_machines:
                self.starting_machine_id = 1

        return machines

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

    def _is_fully_executed(self, job_id):
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
















