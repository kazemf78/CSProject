from dynamic_object import DynamicObject


class TaskGenerator(DynamicObject):
    def pass_time(self):
        pass

    def __init__(self, clock, generation_rate, type_one_rate):
        self.clock = clock
        self.generation_rate = generation_rate
        self.type_one_rate = type_one_rate
        self.time_to_generate = 0
        self.new_task = None

    def generate_task(self):
        """
        waits until some time_to_generate passed
        then generates a new task and puts it in self.new_task
        """
    pass

    

