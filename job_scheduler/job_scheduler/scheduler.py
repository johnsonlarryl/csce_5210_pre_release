import matplotlib.pyplot as plt
import networkx as nx
from networkx import DiGraph
from networkx.readwrite import json_graph
import numpy as np
from typing import List, Tuple, Union

from job_scheduler.model import Job, JobTracker, Operation, PARALLEL_MACHINES, Schedule
from job_scheduler.optimizer import ScheduleOptimizer


class JobScheduler:
    def __init__(self,
                 schedule: Schedule,
                 num_ops_per_machine: int,
                 num_of_machines: int = 0,
                 num_of_jobs: int = 0,
                 num_of_operations_per_job: int = 0,
                 debug: bool = False
                 ) -> Schedule:

        self.debug = debug
        self.num_of_machines = num_of_machines
        self.num_of_jobs = num_of_jobs
        self.num_of_operations_per_machine = num_ops_per_machine

        if not schedule:
            generated_jobs = JobScheduler._generate_jobs(num_of_jobs,
                                                         num_ops_per_machine,
                                                         num_of_operations_per_job)

            self.schedule = Schedule(jobs=generated_jobs)
        else:
            self.schedule = schedule

        self.schedule_optimizer = ScheduleOptimizer()
        self.current = None
        self.next = None
        self.makespan = 0
        self.job_tracker: List[JobTracker]





    @staticmethod
    def _generate_jobs(num_of_jobs: int,
                       num_of_operations_per_machine: int,
                       num_of_operations_per_job: int) -> List[Job]:
        generated_jobs = []

        for job_id in np.random.permutation(np.array(range(1, num_of_jobs + 1))):
            generated_operations = JobScheduler._generate_operations(num_of_operations_per_machine,
                                                                     num_of_operations_per_job)

            generated_jobs.append(Job(id=job_id, operations=generated_operations))

        return generated_jobs

    # @staticmethod
    # def _generate_operations(num_of_operations_per_machine: int,
    #                          num_of_operations_per_job: int) -> List[Operation]:
    #     operations = DiGraph()
    #
    #     for i in num_of_operations_per_job:
    #
    #
    #     for _ in range(0, num_of_operations):
    #         generated_operations.append(Operation())
    #
    #     return

    @staticmethod
    def _process_job(schedule: Schedule) -> None:
        JobScheduler._successor(schedule)

    @staticmethod
    def _successor(schedule: Schedule) -> Operation:
        return schedule.current_job

    @staticmethod
    def _allocate_ops_to_machines(schedule: Schedule) -> Operation:
        return schedule.next_job

    def compute_idle_time(self):
        idle_time = 0

        for job in self.job_tracker:
            idle_time += job.idle_time

        return idle_time

    @staticmethod
    def load_graph(schedule: str):
        return json_graph.node_link_graph(schedule, directed=True)

    @staticmethod
    def visualize_schedule(job: DiGraph, fig_size: Tuple = (12, 8)) -> None:

        pos = nx.nx_agraph.graphviz_layout(job, prog='dot')
        plt.figure(figsize=fig_size)

        nx.draw(job, pos, with_labels=True, node_size=600, node_color="lightblue", font_size=10, arrows=True)

        # Edge labels workaround for potential multiedge issue
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
















