class TimingServer:
    def __init__(self, clock, timing_rate, servers_rates_matrix):
        self.rate = timing_rate
        self.clock = clock
        self.time_to_allocate = 0
        self.tasks = list()
        self.servers = list()
        self.selected_server = None
        # TODO(initialize servers)

    def enqueue_task(self, task):
        """
        get a new task
        :param task: the new task
        """
        pass

    def find_best_server(self):
        """
        selects server with shortest queue as self.selected_server
        :return:
        """
        pass

    def allocate_task_to_server(self):
        """
        after some time_to_allocate passed,
        allocates a task to self.selected_server
        """
        pass

    def pass_time(self):
        """
        makes change in servers state each turn
        """
