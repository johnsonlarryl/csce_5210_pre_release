from job_scheduler.model import Schedule


class ScheduleOptimizer:
    def __init__(self, number_of_operations_per_machine):
        self.number_of_operations_per_machine = number_of_operations_per_machine

    @staticmethod
    def analyze_schedule(schedule: Schedule) -> None:
        """
        Generates a neighboring solution to the current solution
        Takes two random points (jobs) in the existing job schedule and swaps their order

        :param schedule
        :return None
        """
        current_job = ScheduleOptimizer._successor(schedule)








