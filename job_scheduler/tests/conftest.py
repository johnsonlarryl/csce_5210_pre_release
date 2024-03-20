import pytest
from typing import List

from job_scheduler.model import Job, Operation, Schedule, ScheduledJob
from job_scheduler.scheduler import JobScheduler


@pytest.fixture
def schedule() -> Schedule:
    # Job 4
    job_4_schedule_json = \
        {
            "directed": True,
            "nodes": [
                {"id": "start"},
                {"id": "J411"},
                {"id": "J421"},
                {"id": "J422"},
            ],
            "links": [
                {"source": "start", "target": "J411", "weight": 2,
                 "parallel_machines": [("start", "J421"), ("start", "J411")]},
                {"source": "start", "target": "J421", "weight": 2,
                 "parallel_machines": [("start", "J421"), ("start", "J411")]},
                {"source": "J411", "target": "J422", "weight": 2,
                 "parallel_machines": [("J421", "J422"), ("J411", "J422")]},
                {"source": "J421", "target": "J422", "weight": 0,
                 "parallel_machines": [("J421", "J422"), ("J411", "J422")]},
            ]
        }

    j4_schedule = JobScheduler.load_graph(job_4_schedule_json)

    # Job 1
    job_1_schedule_json = \
        {
            "directed": True,
            "nodes": [
                {"id": "J422"},
                {"id": "J111"},
                {"id": "J121"},
                {"id": "J112"},
                {"id": "J122"},
                {"id": "J123"},
            ],
            "links": [
                {"source": "J422", "target": "J111", "weight": 2,
                 "parallel_machines": [("J422", "J111"), ("J422", "J121")]},
                {"source": "J422", "target": "J121", "weight": 2,
                 "parallel_machines": [("J422", "J111"), ("J422", "J121")]},
                {"source": "J111", "target": "J112", "weight": 2,
                 "parallel_machines": [("J111", "J112"), ("J121", "J122")]},
                {"source": "J121", "target": "J122", "weight": 2,
                 "parallel_machines": [("J111", "J112"), ("J121", "J122")]},
                {"source": "J122", "target": "J112", "weight": 0,
                 "parallel_machines": [("J122", "J112"), ("J112", "J123")]},
                {"source": "J112", "target": "J123", "weight": 2,
                 "parallel_machines": [("J122", "J112"), ("J112", "J123")]},
            ]
        }

    j1_schedule = JobScheduler.load_graph(job_1_schedule_json)

    # Job 5
    job_5_schedule_json = \
        {
            "directed": True,
            "nodes": [
                {"id": "J511"},
                {"id": "J512"},
                {"id": "J513"},
                {"id": "J514"},
                {"id": "J521"},
                {"id": "J522"},
                {"id": "J523"},
                {"id": "J524"},
            ],
            "links": [
                {"source": "J123", "target": "J511", "weight": 2,
                 "parallel_machines": [("J123", "J511"), ("J123", "J521")]},
                {"source": "J123", "target": "J521", "weight": 2,
                 "parallel_machines": [("J123", "J511"), ("J123", "J521")]},
                {"source": "J511", "target": "J512", "weight": 2,
                 "parallel_machines": [("J511", "J512"), ("J521", "J522")]},
                {"source": "J521", "target": "J522", "weight": 2,
                 "parallel_machines": [("J511", "J512"), ("J521", "J522")]},
                {"source": "J512", "target": "J513", "weight": 2,
                 "parallel_machines": [("J512", "J513"), ("J522", "J523")]},
                {"source": "J522", "target": "J523", "weight": 2,
                 "parallel_machines": [("J512", "J513"), ("J522", "J523")]},
                {"source": "J513", "target": "J514", "weight": 2,
                 "parallel_machines": [("J513", "J514"), ("J523", "J524")]},
                {"source": "J523", "target": "J524", "weight": 2,
                 "parallel_machines": [("J513", "J514"), ("J523", "J524")]},
            ]
        }

    j5_schedule = JobScheduler.load_graph(job_5_schedule_json)

    # Job 3
    job_3_schedule_json = \
        {
            "directed": True,
            "nodes": [
                {"id": "J514"},
                {"id": "J524"},
                {"id": "J311"},
                {"id": "J312"},
            ],
            "links": [
                {"source": "J514", "target": "J311", "weight": 2,
                 "parallel_machines": [("J514", "J311"), ("J524", "J321")]},
                {"source": "J524", "target": "J321", "weight": 2,
                 "parallel_machines": [("J514", "J311"), ("J524", "J321")]},
                {"source": "J311", "target": "J312", "weight": 1,
                 "parallel_machines": [("J311", "J312"), ("J321", "J312")]},
                {"source": "J321", "target": "J312", "weight": 0,
                 "parallel_machines": [("J311", "J312"), ("J321", "J312")]},
            ]
        }

    j3_schedule = JobScheduler.load_graph(job_3_schedule_json)

    # Job 2

    job_2_schedule_json = \
        {
            "directed": True,
            "nodes": [
                {"id": "J312"},
                {"id": "J211"},
                {"id": "J212"},
                {"id": "J213"},
                {"id": "J214"},
                {"id": "J215"},
                {"id": "J221"},
            ],
            "links": [
                {"source": "J312", "target": "J221", "weight": 1,
                 "parallel_machines": [("J312", "J221"), ("J312", "J211")]},
                {"source": "J312", "target": "J211", "weight": 2,
                 "parallel_machines": [("J312", "J221"), ("J312", "J211")]},
                {"source": "J211", "target": "J212", "weight": 2,
                 "parallel_machines": [("J211", "J212"), ("J221", "J213")]},
                {"source": "J221", "target": "J213", "weight": 2,
                 "parallel_machines": [("J211", "J212"), ("J221", "J213")]},
                {"source": "J213", "target": "J215", "weight": 2,
                 "parallel_machines": [("J213", "J215"), ("J212", "J214")]},
                {"source": "J212", "target": "J214", "weight": 2,
                 "parallel_machines": [("J213", "J215"), ("J212", "J214")]},
            ]
        }

    j2_schedule = JobScheduler.load_graph(job_2_schedule_json)

    jobs = [Job(id=4, operations=j4_schedule),
            Job(id=1, operations=j1_schedule),
            Job(id=5, operations=j5_schedule),
            Job(id=3, operations=j3_schedule),
            Job(id=2, operations=j2_schedule)]

    schedule = Schedule(jobs=jobs)

    return schedule


@pytest.fixture()
def scheduled_jobs() -> List[ScheduledJob]:
    job_1 = ScheduledJob(job_id=1, operations=[Operation(id=1, time=3), Operation(id=2, time=6)])
    job_2 = ScheduledJob(job_id=2, operations=[Operation(id=1, time=10), Operation(id=2, time=1)])
    job_3 = ScheduledJob(job_id=3, operations=[Operation(id=1, time=3), Operation(id=2, time=2)])
    job_4 = ScheduledJob(job_id=4, operations=[Operation(id=1, time=2), Operation(id=2, time=4)])
    job_5 = ScheduledJob(job_id=5, operations=[Operation(id=1, time=8), Operation(id=2, time=8)])

    job_operations = [job_1, job_2, job_3, job_4, job_5]

    return job_operations


@pytest.fixture()
def job_scheduler(scheduled_jobs: List[ScheduledJob]) -> JobScheduler:
    return JobScheduler(num_of_machines=2,
                        num_ops_per_machine=2,
                        scheduled_jobs=scheduled_jobs)
