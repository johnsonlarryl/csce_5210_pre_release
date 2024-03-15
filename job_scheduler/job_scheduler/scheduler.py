import matplotlib.pyplot as plt
import networkx as nx
from networkx import DiGraph
from networkx.readwrite import json_graph
import numpy as np
from typing import List

from job_scheduler.model import Job, JobTracker, Machine, Operation, Schedule
from job_scheduler.optimizer import ScheduleOptimizer


class JobScheduler:
    def __init__(self, num_of_jobs: int,
                 num_of_operations: int,
                 num_of_operations_per_machine: int,
                 num_of_operations_per_job: int,
                 temperature: int = 1000) -> Schedule:
        self.num_of_operations = num_of_operations
        self.num_of_jobs = num_of_jobs
        self.num_of_operations_per_machine = num_of_operations_per_machine

        generated_jobs = JobScheduler._generate_jobs(num_of_jobs,
                                                     num_of_operations,
                                                     num_of_operations_per_machine,
                                                     num_of_operations_per_job)

        self.schedule = Schedule(jobs=generated_jobs)
        self.temperature = temperature
        self.schedule_optimizer = ScheduleOptimizer()
        self.current = None
        self.next = None
        self.makespan = 0
        self.job_tracker: List[JobTracker]

    def execute_schedule(self, schedule_iterations: int = 400) -> int:
        for schedule_iteration in range(1, schedule_iterations):
            JobScheduler._process_job(self.schedule)



    @staticmethod
    def _generate_jobs(num_of_jobs: int,
                       num_of_operations: int,
                       num_of_operations_per_machine: int,
                       num_of_operations_per_job: int) -> List[Job]:
        generated_jobs = []

        for job_id in np.random.permutation(np.array(range(1, num_of_jobs + 1))):
            generated_operations = JobScheduler._generate_operations(num_of_operations,
                                                                     num_of_operations_per_machine,
                                                                     num_of_operations_per_job)

            generated_jobs.append(Job(id=job_id, operations=generated_operations))

        return generated_jobs

    # @staticmethod
    # def _generate_operations(num_of_operations: int,
    #                          num_of_operations_per_machine: int,
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

    @staticmethod
    def _minimize_execution_time(schedule: Schedule):
        delta_E = JobScheduler.compute_step_makespan(schedule.next_op_scheduled) - \
                  JobScheduler.compute_step_makespan(schedule.current_op_scheduled)

    @staticmethod
    def compute_step_makespan(operation: Operation,
                              num_of_operations_per_machine: int) -> int:
        return min(operation.time, num_of_operations_per_machine)

    # def compute_total_makespan(self):
    #     for self.schedule

    def compute_idle_time(self):
        idle_time = 0

        for job in self.job_tracker:
            idle_time += job.idle_time

        return idle_time

    @staticmethod
    def load_graph(schedule: str):
        return json_graph.node_link_graph(schedule, directed=True)

    @staticmethod
    def visualize_schedule(schedule: DiGraph, operation_size=550, location_font_size=10, operation_widths=1) -> None:
        links = [(u, v) for (u, v, d) in schedule.edges(data=True)]
        pos = nx.spring_layout(schedule)
        nx.draw_networkx_nodes(schedule,
                               pos,
                               node_size=operation_size,
                               node_color='lightblue',
                               linewidths=0.25)
        nx.draw_networkx_edges(schedule, pos, edgelist=links, width=operation_widths)

        nx.draw_networkx_labels(schedule, pos, font_size=location_font_size, font_family="sans-serif")

        edge_labels = dict(((u, v), d['weight']) for u, v, d in schedule.edges(data=True))
        nx.draw_networkx_edge_labels(schedule, pos, edge_labels)

        plt.show()
















