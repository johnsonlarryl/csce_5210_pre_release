from job_scheduler.scheduler import JobScheduler


def test_generate_schedule(job_scheduler: JobScheduler):
    schedule = job_scheduler.generate_schedule()

    expect_make_span = 27

    actual_makespan = schedule.compute_makespan()

    assert expect_make_span == actual_makespan

