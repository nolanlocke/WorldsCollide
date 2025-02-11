from objectives.results._objective_result import *
from objectives.results._apply_characters_party import ApplyToParty

class Field(field_result.Result):
    def src(self):
        from data.characters import Characters
        src = [
            field.AddStatusEffects(Characters.PARTY0, field.Status.IMP),
            field.AddStatusEffects(Characters.PARTY1, field.Status.IMP),
            field.AddStatusEffects(Characters.PARTY2, field.Status.IMP),
            field.AddStatusEffects(Characters.PARTY3, field.Status.IMP),
        ]
        return src

class Battle(battle_result.Result):
    def src(self):
        character_status_start = 0x1614
        imp_mask = 0x20

        src = ApplyToParty([
            asm.LDA(character_status_start, asm.ABS_Y), # load character's current status effect bits
            asm.ORA(imp_mask, asm.IMM8),                # apply imp status effect
            asm.STA(character_status_start, asm.ABS_Y), # save status effects
        ])
        return src

class Result(ObjectiveResult):
    NAME = "Imp Song"
    def __init__(self):
        super().__init__(Field, Battle)
