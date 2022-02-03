from objectives.conditions._objective_condition import *
from constants.objectives.condition_bits import dragon_bit

class Condition(ObjectiveCondition):
    NAME = "Dragon"
    def __init__(self, dragon):
        self.dragon = dragon
        self.value = self.dragon
        super().__init__(ConditionType.BattleBit, self.bit())

    def __str__(self):
        return super().__str__(self.dragon)

    def dragon_name(self):
        return dragon_bit[self.dragon].name

    def bit(self):
        return dragon_bit[self.dragon].bit

    def name(self):
        return self.dragon_name()

