from typing import List

from job_scheduler.model import ScheduledJobs
from job_scheduler.scheduler import JobScheduler


def test_map_job(scheduled_jobs: List[ScheduledJobs]):
    job_scheduler = JobScheduler(num_of_machines=2,
                                 num_ops_per_machine=2,
                                 scheduled_jobs=scheduled_jobs)

    schedule = job_scheduler._map_schedule()

