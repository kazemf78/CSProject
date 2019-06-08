from processing_core import ProcessingCore


class ProcessingServer:
    def __init__(self, clock, service_rate, pc_rates):
        self.clock = clock  # TODO(remove clock)
        self.service_rate = service_rate
        self.queue = None  # TODO(appropriate implementation)
        self.cores = list()
        for rate in pc_rates:
            self.cores.append(ProcessingCore(rate, clock))

    def allocate_task(self):
        """
        allocates one task from queue to one of idle cores
        """
        pass

    def enqueue_task(self, task):
        """
        adds a new task to queue
        :param task: new task
        task.server_assignment_time is set here
        """
        pass

    def check_tasks_deadlines(self):
        """
        removes tasks with passed deadlines from queue
        """
        pass

    def pass_time(self):
        """
        makes changes in server and cores each turn when called
        """
        self.check_tasks_deadlines()
        self.allocate_task()

        for core in self.cores:
            core.pass_time()
