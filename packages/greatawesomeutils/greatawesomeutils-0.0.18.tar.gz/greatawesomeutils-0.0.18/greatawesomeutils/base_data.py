from itertools import cycle
import random

class BaseData():
    def get_data(self):
        pass

    def __init__(self):
        self.has_initialized  = True
        data = self.get_data()
        random.shuffle(data)
        self.data = data
        self.cycled_data = cycle(self.data)

    def get_one(self):
        return next(self.cycled_data)

    def get_unique_random(self):
        ls   = [dict(s) for s in set(frozenset(d.items()) for d in self.data)]
        return random.choice(ls)

    def get_unique_random_value(self):
        return next(iter(self.get_unique_random().values()))

    def get_hundred(self):
        return self.data


    def get_n(self, n):
        ls = []
        for i in range(n):
            ls.append(self.get_one())
        return ls