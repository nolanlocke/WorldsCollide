from objectives.conditions._objective_condition import *
from constants.objectives.condition_bits import boss_bit

class Condition(ObjectiveCondition):
    NAME = "Boss"
    def __init__(self, boss):
        self.boss = boss
        self.value = self.boss
        super().__init__(ConditionType.BattleBit, self.bit())

    def __str__(self):
        return super().__str__(self.boss)

    def boss_name(self):
        return boss_bit[self.boss].name

    def bit(self):
        return boss_bit[self.boss].bit

    def name(self):
        return self.boss_name()