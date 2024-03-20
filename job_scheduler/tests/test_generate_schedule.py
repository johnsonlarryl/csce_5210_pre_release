from job_scheduler.scheduler import JobScheduler


def test_generate_schedule(job_scheduler: JobScheduler):
    schedule = job_scheduler.generate_schedule()

    print(schedule.compute_makespan())

    pass

