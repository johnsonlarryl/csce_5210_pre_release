from job_scheduler.model import Schedule


def test_compute_makespan(schedule: Schedule) -> None:
    expect_make_span = 27
    actual_make_span = schedule.compute_makespan()

    assert actual_make_span == expect_make_span
