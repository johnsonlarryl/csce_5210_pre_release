from job_scheduler.model import Schedule
from job_scheduler.optimizer import ScheduleOptimizer


def test_optimzer(schedule: Schedule) -> None:
    schedule_optimzer = ScheduleOptimizer(schedule=schedule)
    default_make_span = schedule.compute_makespan()
    optimized_make_span = schedule_optimzer.optimize()

    assert optimized_make_span <= default_make_span

    print(f"New Schedule makespan: {schedule_optimzer._current_schedule.compute_makespan()}")

    schedule_optimzer.get_boltzmann_distributon()

    pass
