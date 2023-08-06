from base import profile, start

class NoSlots:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = (1, 2, 34)

class Slots:
    __slots__ = ['a', 'b', 'c']
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = (1, 2, 34)

@profile()
def class_slots():
    xs = [Slots() for _ in range(0, 100_000)]
    return xs

@profile()
def class_no_slots():
    xs = [NoSlots() for _ in range(0, 100_000)]
    return xs

if __name__ == '__main__':
    start(__file__, __name__, locals())