class VariableBank:
    def __init__(self):
        self._bank = {}

    def __getitem__(self, key):
        return self._bank[key]

    def defined(self, key):
        return key in self._bank