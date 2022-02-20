from constants.objectives.conditions import ObjectiveConditionType
from data.text.text1 import text_value
from memory.rom import ROM
from memory.space import Allocate, Bank
from utils.flatten import flatten
from objectives.conditions._objective_condition import ObjectiveCondition

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
        if byte < 0:
            val = bytearray.fromhex(hex(~byte).lstrip('0x').rstrip('L').zfill(4))
            return [val[0] | 8, val[1]]
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
        # write down the name found in the menu
        name_space = self.allocate_name(objective.result.__str__())
        # write down the result NAME (this is more or less an ID)
        type_name_space = self.allocate_name(objective.result.NAME)

        [name_ptr_high_byte, name_ptr_low_byte]= self.get_high_low_bytes(name_space.start_address - NAME_BANK_INT)
        [type_name_ptr_high_byte, type_name_ptr_low_byte]= self.get_high_low_bytes(type_name_space.start_address - NAME_BANK_INT)

        count = getattr(objective.result, 'count', None)
        levels = getattr(objective.result, 'levels', None)

        new_data = flatten([
            # $00
            objective.id,
            # $01-$02
            name_ptr_high_byte, # high byte of pointer
            name_ptr_low_byte, # low byte of pointer
            # $03
            len(objective.conditions), # number of conditions affecting objective
            # $04
            objective.conditions_required, # number of conditions required
            # $05-$06 the result value for the objective 0xFFFF is null
            self.get_high_low_bytes(count or levels or 0xffff),
            # $07-$08
            type_name_ptr_high_byte,
            type_name_ptr_low_byte,
            [255 for f in range(0, 23)]
        ])

        objective_data += new_data

        for index in range(len(objective.conditions)):
            condition = objective.conditions[index]
            objective_data += self.get_objective_condition_metadata(condition, index)

        return [objective, objective_data]

    def get_objective_condition_metadata(self, condition: ObjectiveCondition, index):
        condition_data = []
        this_condition_data = []
        condition_type_value = condition.condition_type.value

        name_space = self.allocate_name(condition.__str__())
        [name_ptr_high_byte, name_ptr_low_byte]= self.get_high_low_bytes(name_space.start_address - NAME_BANK_INT)
        type_name_space = self.allocate_name(condition.NAME)
        [type_name_ptr_high_byte, type_name_ptr_low_byte]= self.get_high_low_bytes(type_name_space.start_address - NAME_BANK_INT)


        this_condition_data += [
            # $00 arbitrary id
            index,
            # $01-$02 pointer to name (offset 0xFE0000)
            name_ptr_high_byte,
            name_ptr_low_byte,
            # $03 condition type enum value - used for data manipulation when reading bits
            condition_type_value if condition.condition_type == ObjectiveConditionType.BattleBit
            else condition_type_value if condition.condition_type == ObjectiveConditionType.Character
            else condition_type_value if condition.condition_type == ObjectiveConditionType.Esper
            else condition_type_value if condition.condition_type == ObjectiveConditionType.EventBit
            else condition_type_value if condition.condition_type == ObjectiveConditionType.EventWord
            else 255,
            # $04-$05 the base address in memory
            self.get_high_low_bytes(condition.base_address()),
            # $06-$07 the bit offset in memory
            self.get_high_low_bytes(condition.bit()),
            # $07-$08 the context value. Used with condition type
            self.get_high_low_bytes(getattr(condition, 'value', 0xffff)),
            type_name_ptr_high_byte,
            type_name_ptr_low_byte,
            [255 for f in range(0, 4)]
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
            10, # $00 arbitrary id
            int(OBJECTIVE_BANK, 16), # $01 bank of objective data
            None, # $02 high byte - offset for start of objective data (from start of bank)
            None, # $03 low  byte - offset for start of objective data (from start of bank)
            None, # $04 high byte - size of objective data
            None, # $05 low  byte - size of objective data
            len(self.objectives), # $06
            [255 for f in range(0, 9)]
        ])

        header_space = Allocate(Bank[HEADER_BANK], len(header), "Objective Header")
        objective_space = Allocate(Bank[OBJECTIVE_BANK], len(objective_data), f"Objective Metadata", 0xFF)
        # set $02-$03
        header[2:4] = self.get_high_low_bytes(objective_space.start_address - OBJECTIVE_BANK_INT)
        # set $04-$05
        header[4:6] = self.get_high_low_bytes(len(objective_data))
        header_space.write(header)
        objective_space.write(objective_data)

    def __len__(self):
        return len(self.objectives)

    def __getitem__(self, index):
        return self.objectives[index]

    def post_write_assert(self):
        return self.rom.get_bytes()
