from constants.objectives.conditions import ConditionType, ObjectiveConditionType
from data.text.text1 import text_value
from memory.rom import ROM
from memory.space import Allocate, Bank
from utils.flatten import flatten

OBJECTIVE_BANK = "FF"
NAME_BANK = "FE"
HEADER_BANK = "FF"
OBJECTIVE_BANK_INT = (int(OBJECTIVE_BANK, 16) << 16) - 0xC00000
NAME_BANK_INT = (int(NAME_BANK, 16) << 16) - 0xC00000
HEADER_BANK_INT = (int(HEADER_BANK, 16) << 16) - 0xC00000

OBJECTIVE_HEADER_LENGTH = 31
OBJECTIVE_NAME_LENGTH = 31
CONDITION_NAME_LENGTH = 31

class ObjectiveMetadataWriter:
    def get_high_low_bytes(self, byte):
        val = bytearray.fromhex(hex(byte).lstrip('0x').rstrip('L').zfill(4))
        return [val[0], val[1]]

    def __init__(self, rom: ROM, args):
        from objectives.objectives import Objectives
        from objectives.objective import Objective
        self.args = args
        self.rom = rom
        self.objectives: list[Objective] = Objectives().objectives
        self.name_spaces = {}

    def get_objective_metadata(self, index):
        from objectives.objective import Objective
        from objectives.objectives import Objectives
        objective = Objective(index)

        # if objective.result.NAME not in Objectives.results:
        #     Objectives.results[objective.result.NAME] = [objective]
            # Objectives.results[objective.result.NAME].append(objective)
        # else:

        objective_data = []
        name_space = self.allocate_name(objective.result.NAME)
        value = getattr(objective.result, 'count', 255)

        [name_ptr_high_byte, name_ptr_low_byte]= self.get_high_low_bytes(name_space.start_address - NAME_BANK_INT)
        new_data = flatten([
            objective.id,
            name_ptr_high_byte, # high byte of pointer
            name_ptr_low_byte, # low byte of pointer
            len(objective.conditions), # number of conditions affecting objective
            objective.conditions_required, # number of conditions required
            [255 for f in range(0, 27)]
        ])

        objective_data += new_data

        for index in range(len(objective.conditions)):
            condition = objective.conditions[index]
            objective_data += self.get_objective_condition_metadata(condition, index)

        return [objective, objective_data]

    def get_objective_condition_metadata(self, condition, index):
        condition_data = []
        this_condition_data = []
        condition_type_value = condition.condition_type.value

        name_space = self.allocate_name(condition.NAME)
        [name_ptr_high_byte, name_ptr_low_byte]= self.get_high_low_bytes(name_space.start_address - NAME_BANK_INT)

        this_condition_data += [
            index,
            name_ptr_high_byte,
            name_ptr_low_byte,
            condition_type_value if condition.condition_type == ObjectiveConditionType.BattleBit
            else condition_type_value if condition.condition_type == ObjectiveConditionType.Character
            else condition_type_value if condition.condition_type == ObjectiveConditionType.Esper
            else condition_type_value if condition.condition_type == ObjectiveConditionType.EventBit
            else condition_type_value if condition.condition_type == ObjectiveConditionType.EventWord
            else 255,
            self.get_high_low_bytes(condition.base_address()),
            self.get_high_low_bytes(condition.bit()),
            self.get_high_low_bytes(getattr(condition, 'value', 0xffff)),
            [255 for f in range(0, 6)]
        ]

        this_condition_data = flatten(this_condition_data)

        get_name = getattr(condition, 'name', None)
        if get_name:
            space = self.allocate_name(get_name())
            this_condition_data[10:12] = self.get_high_low_bytes(space.start_address - NAME_BANK_INT)

        condition_data += this_condition_data

        return condition_data

    def allocate_name(self, target_name):
        cached = self.name_spaces.get(target_name)
        if cached:
            return cached

        obj_name = [len(target_name)] + [ord(s) for s in target_name] + [10, 10] # first byte length of text, terminate with 2 newline characters
        space_to_write = Allocate(Bank[NAME_BANK], len(obj_name), f"Write name '{target_name}'", 0xFF)

        self.name_spaces[target_name] = space_to_write

        space_to_write.write(obj_name)

        return space_to_write

    def write(self):
        objective_data = []
        name_data = []
        for index in range(0, len(self.objectives)):
            [objective, data] = self.get_objective_metadata(index)
            objective_data += flatten(data)

        header = flatten([
            10, # id
            int(OBJECTIVE_BANK, 16), # bank of objective data
            2, # high byte - offset for start of objective data (from start of bank)
            3, # low  byte - offset for start of objective data (from start of bank)
            4, # high byte - size of objective data
            5, # low  byte - size of objective data
            len(self.objectives),
            [255 for f in range(0, 9)]
        ])

        header_space = Allocate(Bank[HEADER_BANK], len(header), "Objective Header")
        objective_space = Allocate(Bank[OBJECTIVE_BANK], len(objective_data), f"Objective Metadata", 0xFF)
        header[2:4] = self.get_high_low_bytes(objective_space.start_address - OBJECTIVE_BANK_INT)
        header[4:6] = self.get_high_low_bytes(len(objective_data))
        header_space.write(header)
        objective_space.write(objective_data)

    def __len__(self):
        return len(self.objectives)

    def __getitem__(self, index):
        return self.objectives[index]

    def post_write_assert(self):
        return self.rom.get_bytes()
