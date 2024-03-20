from typing import List

from job_scheduler.model import ScheduledJob
from job_scheduler.optimizer import ScheduleOptimizer
from job_scheduler.scheduler import JobScheduler


def test_optimzer(scheduled_jobs: List[ScheduledJob],
                  job_scheduler: JobScheduler):
    schedule_optimzer = ScheduleOptimizer(scheduled_jobs=scheduled_jobs,
                                          num_of_machines=2,
                                          num_ops_per_machine=2)

    schedule = job_scheduler.generate_schedule()
    default_make_span = schedule.compute_makespan()
    optimized_make_span = schedule_optimzer.optimize()

    assert optimized_make_span <= default_make_span

    print(f"New Schedule makespan: {schedule_optimzer._current_schedule.compute_makespan()}")

    schedule_optimzer.get_boltzmann_distributon()
