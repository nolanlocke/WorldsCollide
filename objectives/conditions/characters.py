from objectives.conditions._objective_condition import *
import random

class Condition(ObjectiveCondition):
    NAME = "Characters"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        self.value = self.count
        super().__init__(ConditionType.EventWord, self.bit(), self.count)

    def __str__(self):
        return super().__str__(self.count)

    def bit(self):
        return event_word.CHARACTERS_AVAILABLE
