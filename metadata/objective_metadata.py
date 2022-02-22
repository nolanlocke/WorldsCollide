
from metadata.objective_condition_metadata import ObjectiveConditionMetadata
from objectives.objective import Objective

class ObjectiveMetadata:
    def __init__(self, objective: Objective):
        self.objective = objective
        self.id = objective.id
        self.NAME = objective.result.NAME
        self.conditions = [ObjectiveConditionMetadata(c) for c in objective.conditions]
        self.conditions_required = objective.conditions_required

    def to_json(self):
        return {
            'id': self.id,
            'name': self.NAME,
            'conditions': [c.to_json() for c in self.conditions],
            'conditions_required': self.conditions_required
        }