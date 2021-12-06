class Space:
    def __init__(self, min_range, max_range, step):
        self.min_range = min_range
        self.max_range = max_range
        self.step = step

    def __str__(self):
        return f'Space object in range [{self.min_range}; {self.max_range}] with step: {self.step}'
