from objectives.conditions._objective_condition import ObjectiveCondition

class ObjectiveConditionMetadata:
    def __init__(self, condition: ObjectiveCondition):
        self.condition = condition
        self.condition_type_name = condition.condition_type.name
        self.condition_type_value = condition.condition_type.value
        if hasattr(condition, 'count'):
            self.value = condition.count
        elif hasattr(condition, 'value'):
            self.value = condition.value
        self.NAME = condition.NAME
        self.base_address = condition.base_address()
        self.bit = condition.bit()

    def to_json(self):
        return {
            'condition_type_name': self.condition_type_name,
            'condition_type_value': self.condition_type_value,
            'value': self.value,
            'name': str(self.condition),
            'base_address': self.base_address,
            'bit': self.bit
        }
