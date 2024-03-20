from job_scheduler.scheduler import JobScheduler


def test_generate_schedule(job_scheduler: JobScheduler):
    schedule = job_scheduler.generate_schedule()

    expect_make_span = 27

    actual_makespan = schedule.compute_makespan()

    assert expect_make_span == actual_makespan


def test_generate_random_schedules():
    scheduled_jobs = JobScheduler.generate_scheduled_jobs(num_of_jobs=50,
                                                          num_of_operations_per_job=3)

    job_scheduler = JobScheduler(scheduled_jobs=scheduled_jobs,
                                 num_of_machines=5,
                                 num_ops_per_machine=3)

    schedule = job_scheduler.generate_schedule()

    assert schedule is not None

    assert schedule.compute_makespan() > 0

    scheduled_jobs = JobScheduler.generate_scheduled_jobs(num_of_jobs=50,
                                                          num_of_operations_per_job=5)

    job_scheduler = JobScheduler(scheduled_jobs=scheduled_jobs,
                                 num_of_machines=3,
                                 num_ops_per_machine=5)

    schedule = job_scheduler.generate_schedule()

    assert schedule is not None

    assert schedule.compute_makespan() > 0




