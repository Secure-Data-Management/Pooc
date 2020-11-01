from PBC.ECC.field import Field


class Element:
    def __init__(self, field: Field, data):
        self.field = field
        self.data = data

    def __mul__(self, other):
        pass
