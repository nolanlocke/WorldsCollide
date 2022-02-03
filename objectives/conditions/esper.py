from objectives.conditions._objective_condition import *
from constants.espers import id_esper
class Condition(ObjectiveCondition):
    NAME = "Esper"
    def __init__(self, esper):
        self.esper = esper
        self.value = self.esper
        super().__init__(ConditionType.Esper, self.bit())

    def __str__(self):
        return super().__str__(self.esper)

    def esper_name(self):
        # TODO: Need to alphabetize these instead
        return id_esper[self.esper]

    def bit(self):
        return self.esper

    def name(self):
        return self.esper_name()