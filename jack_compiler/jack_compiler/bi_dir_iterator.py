class BiDirIter:
    def __init__(self, items):
        self.some_items = [i for i in range(20)]
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index >= len(self.some_items):
            raise StopIteration
        return self.some_items[self.index]

    def move_backward(self):
        if self.index > -1:
            self.index -= 1


if __name__ == "__main__":
    bid_dir_iter = BiDirIter()
    print(next(bid_dir_iter))
    print(next(bid_dir_iter))
    bid_dir_iter.move_backward()
    print(next(bid_dir_iter))
    for element in bid_dir_iter:
        print(element)