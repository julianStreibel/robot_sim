from .Joint import Joint


class Revolute(Joint):
    def __init__(self, rotation=0):
        super().__init__(rotation)
