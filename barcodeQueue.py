#queue for Barcode

class BarcodeQueue:
    def __init__(self, lst=[]):
        self.data = set()
        if lst: self.data = {lst[i] for i in range(0, len(lst))}

    def add(self, x):
        self.data.add(x)
    def addAll(self, lst):
        for i in range(0, len(lst)): self.data.add(lst[i])
    def poll(self):
        try:
            element = self.data.pop()
        except KeyError as KE:
            return None
        else:
            return element
    def remove(self):
        #will return key error error if data set is empty
        return self.data.pop()
    def peek(self):
        try:
            element = next(iter(self.data))
            return element

        except NameError as NE:
            return None
    def element(self):
        #will return key error if data set is empty
        return self.data.pop()
