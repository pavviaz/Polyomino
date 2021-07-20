
from ortools.sat.python import cp_model


class Solver:
    def __init__(self):
        self.model = cp_model.CpModel()

