import copy
import math
import numpy as np
import random

from job_scheduler.model import Schedule


class ScheduleOptimizer:
    def __init__(self,
                 schedule: Schedule,
                 temperature: int = 1000,
                 schedule_iterations: int = 400):
        self.schedule = schedule
        self._current_schedule = copy.deepcopy(schedule)
        self._next_schedule = copy.deepcopy(schedule)
        self.schedule_iterations = schedule_iterations
        self.temperature = temperature
        self._probability_time_series = []
        self._makespan_time_series = []

    def optimize(self) -> int:
        self._probability_time_series = []
        self._makespan_time_series = []

        self._makespan_time_series.append(self._current_schedule.compute_makespan())

        for i in range(1, self.schedule_iterations):
            self._successor()
            delta_E = self.compute_makespan()

            self._makespan_time_series.append(self._current_schedule.compute_makespan())

            if delta_E > 0:
                self._current_schedule = self._next_schedule
                boltzmann_distributon = 0
            else:
                r = random.random()
                boltzmann_distributon = math.exp(delta_E/self.temperature)

                if boltzmann_distributon <= r:
                    self._current_schedule = self._next_schedule
                    self.boltzmann_distributon_makespan_udpate[i] = self._current_schedule.compute_makespan()

            self._probability_time_series.append(boltzmann_distributon)
            self.temperature *= 0.99

        return self._current_schedule.compute_makespan()

    def _successor(self) -> None:
        current_job_scheduled = self._get_random_job()
        next_job_scheduled = self._get_random_job()

        while next_job_scheduled == current_job_scheduled:
            next_job_scheduled = self._get_random_job()

        current_job = self._current_schedule.jobs[current_job_scheduled]
        next_job = self._current_schedule.jobs[next_job_scheduled]

        self._next_schedule.jobs[current_job_scheduled] = next_job
        self._next_schedule.jobs[next_job_scheduled] = current_job

    def _get_random_job(self):
        return random.randint(0, len(self._current_schedule.jobs) - 1)

    def compute_makespan(self):
        return self._current_schedule.compute_makespan() - self._next_schedule.compute_makespan()

    def get_makespan_time_series(self) -> np.ndarray:
        if len(self._makespan_time_series) > 0:
            return np.array(self._makespan_time_series)
        else:
            return np.empty(0)

    def get_boltzmann_distributon(self) -> np.ndarray:
        if len(self._probability_time_series) > 0:
            return np.array(self._probability_time_series)
        else:
            return np.empty(0)





