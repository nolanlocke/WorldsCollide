from objectives.conditions._objective_condition import *
from constants.objectives.condition_bits import check_bit
from constants.entities import id_name

class Condition(ObjectiveCondition):
    NAME = "Check"
    def __init__(self, check):
        self.check = check
        self.value = self.check
        super().__init__(ConditionType.EventBit, self.bit())

    def __str__(self):
        return super().__str__(self.check)

    def bit(self):
        return check_bit[self.check].bit

    def name(self):
        return check_bit[self.check].name
