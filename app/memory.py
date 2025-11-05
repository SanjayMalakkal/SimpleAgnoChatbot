class SimpleMemory:
    def __init__(self):
        self.store = {}

    def remember(self, key, value):
        self.store[key] = value

    def recall(self, key):
        return self.store.get(key)

    def clear(self):
        self.store.clear()
