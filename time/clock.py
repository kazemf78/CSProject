from time.dynamic_object import DynamicObject


class Clock:
    def __init__(self):
        self.time = 0
        self.registered_objects: [DynamicObject] = list()

    def register(self, obj):
        self.registered_objects.append(obj)

    def pass_time(self):
        for obj in self.registered_objects:
            obj.pass_time()
