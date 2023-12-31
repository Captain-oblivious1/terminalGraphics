from Context import *

class MemoryContext(Context):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = [height][width]
