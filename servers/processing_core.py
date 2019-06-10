from time_.clock import Clock
from time_.dynamic_object import DynamicObject
from task.task import Task


class ProcessingCore(DynamicObject):
    def __init__(self, service_rate, clock):
        self.service_rate = service_rate
        self.clock: Clock = clock
        self.task: Task = None
        self.time_to_finish = 0

    def accept_task(self, task):
        """
        gets a task to execute
        :param task: new task
        task.core_assignment_time is set here
        """
        self.task = task
        # TODO(set time_to_finish)

    def execute_task(self):
        """
        does a part of task if there is one
        task.core_assignment_time is set here

        """
        pass

    def pass_time(self):
        self.execute_task()
