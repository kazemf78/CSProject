class Task:
    def __init__(self, task_type, deadline, creation_time):
        self.type = task_type
        self.deadline = deadline
        self.creation_time = creation_time
        self.server_assignment_time = None
        self.core_assignment_time = None
        self.finish_time = None
