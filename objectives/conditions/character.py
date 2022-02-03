from objectives.conditions._objective_condition import *
from constants.entities import id_name

class Condition(ObjectiveCondition):
    NAME = "Character"
    def __init__(self, character):
        self.character = character
        self.value = character
        super().__init__(ConditionType.Character, self.bit())

    def __str__(self):
        return super().__str__(self.character)

    def bit(self):
        return self.character

    def name(self):
        return id_name[self.character]