"""Set ADT logic: hash table with linear probing (no built-in set operations)."""

SIZE = 10


class HashTable:
    def __init__(self, size=SIZE):
        self.size = size
        self.slots = [None] * size
        self.used = 0

    def hashIt(self, value):
        return value % self.size

    def find(self, value):
        i = self.hashIt(value)
        tries = 0
        while tries < self.size:
            if self.slots[i] is None:
                return -1
            if self.slots[i] == value:
                return i
            i = (i + 1) % self.size
            tries += 1
        return -1

    def insert(self, value):
        if self.find(value) != -1:
            return "duplicate"
        if self.used == self.size:
            return "full"
        i = self.hashIt(value)
        while self.slots[i] != None:
            i = (i + 1) % self.size
        self.slots[i] = value
        self.used += 1
        return "ok"

    def delete_value(self, value):
        i = self.find(value)
        if i == -1:
            return False
        self.slots[i] = None
        self.used -= 1
        j = (i + 1) % self.size
        while self.slots[j] is not None:
            v = self.slots[j]
            self.slots[j] = None
            self.used -= 1
            self.insert(v)
            j = (j + 1) % self.size
        return True

    def getAll(self):
        out = []
        for v in self.slots:
            if v is not None:
                out.append(v)
        return out


class MySet:
    def __init__(self, name):
        self.name = name
        self.table = HashTable()

    def add(self, x):
        return self.table.insert(x)

    def delete(self, x):
        return self.table.delete_value(x)

    def contains(self, x):
        return self.table.find(x) != -1

    def members(self):
        return self.table.getAll()

    def size(self):
        return self.table.used

    # shortcut: every set operation builds Set C from a list of items
    @staticmethod
    def make_c(items):
        c = MySet("C")
        for x in items:
            if c.add(x) == "full":
                raise OverflowError("too many elements")
        return c

    def union(self, other):
        return MySet.make_c(self.members() + other.members())

    def intersection(self, other):
        return MySet.make_c([x for x in self.members() if other.contains(x)])

    def difference(self, other):
        return MySet.make_c([x for x in self.members() if not other.contains(x)])