class CountdownIter:
    """Documentation for CountdownIter
    """
    def __init__(self, count):
        self.count = count

    def __next__(self):
        if self.count <= 0:
            raise StopIteration
        else:
            remain = self.count
            self.count -= 1
            return remain

class Countdown:
    """Documentation for Countdown

    """
    def __init__(self, count):
        self.count = count
    def __iter__(self):
        return CountdownIter(self.count)



if __name__ == "__main__":
    c = Countdown(10)
    for elem in c:
        print(elem, end=" ")


