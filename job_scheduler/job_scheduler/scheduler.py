import json
import matplotlib.pyplot as plt
import networkx as nx
from networkx import DiGraph
from networkx.readwrite import json_graph
import numpy as np
from typing import Any, Dict, List, Tuple, Union

from job_scheduler.model import Job, Operation, PARALLEL_MACHINES, Schedule, ScheduledJobs


class JobScheduler:
    def __init__(self,
                 scheduled_jobs: ScheduledJobs,
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
        pass

        # if not schedule:
        #     generated_jobs = JobScheduler._generate_jobs(num_of_jobs,
        #                                                  num_ops_per_machine,
        #                                                  num_of_operations_per_job)
        #
        #     self.schedule = Schedule(jobs=generated_jobs)
        # else:
        #     self.schedule = schedule
        #
        # self.current = None
        # self.next = None
        # self.makespan = 0
        # self.job_tracker: List[JobTracker]

    def _init_job_allocations(self):
        self.job_allocations = {}

        for i in range(0, len(self.scheduled_jobs.operations)):
            for operation in self.scheduled_jobs.operations[i]:
                if operation.job_id not in self.job_allocations.keys():
                    self.job_allocations[operation.job_id] = {}

                self.job_allocations[operation.job_id][operation.id] = operation.time

    def generate_schedule(self) -> Schedule: pass

    # @staticmethod
    # def _generate_jobs(num_of_jobs: int,
    #                    num_of_operations_per_machine: int,
    #                    num_of_operations_per_job: int) -> List[Job]:
    #     generated_jobs = []
    #
    #     for job_id in np.random.permutation(np.array(range(1, num_of_jobs + 1))):
    #         generated_operations = JobScheduler._generate_operations(num_of_operations_per_machine,
    #                                                                  num_of_operations_per_job)
    #
    #         generated_jobs.append(Job(id=job_id, operations=generated_operations))
    #
    #     return generated_jobs
    #

    def _map_schedule(self) -> Dict: pass

    # def _map_job(self, root=False) -> Dict[Any, Any]:
        # nodes = []
        # links = []
        #
        # if root:
        #     nodes.append({"id": "start"})
        #
        # for i in range(0, len(self.scheduled_jobs.operations)):
        #     machine_allocations = self._init_machine_allocations()
        #
        #     for operation in self.scheduled_jobs.operations[i]:
        #         nodes.append({"id": f"J{operation.job_id}"})
        #
        #         for j in range(1, len(self.num_of_machines + 1)):


    def _generate_nodes(self) -> List[Dict]: pass


    def _init_machine_allocations(self) -> Dict[int, int]:
        machine_allocations = {}

        for j in range(1, len(self.num_of_machines + 1)):
            machine_allocations[j] = self.num_of_operations_per_machine

        return machine_allocations


    @staticmethod
    def _generate_operations(num_of_operations_per_machine: int,
                             num_of_operations_per_job: int) -> List[Operation]:
        pass

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
















