from memory.space import Bank, Write
import instruction.asm as asm
from objectives._cached_function import _CachedFunction

import data.event_bit as event_bit
import data.battle_bit as battle_bit
import data.event_word as event_word

class _Condition(_CachedFunction, asm.JSR):
    def __init__(self, *args, **kwargs):
        _CachedFunction.__init__(self, *args, **kwargs)
        asm.JSR.__init__(self, self.address(*args, **kwargs), asm.ABS)

class _BitCondition(_Condition):
    def write(self, address, bit, true, false):
        if true is None:
            true = []
        if false is None:
            false = []

        src = [
            asm.LDA(address, asm.ABS),
            asm.AND(2 ** bit, asm.IMM8),
            asm.BEQ("FALSE"),

            true,
            asm.RTS(),

            "FALSE",
            false,
            asm.RTS(),
        ]
        return Write(Bank.F0, src, f"battle bit condition {hex(address)} {hex(bit)}")

class EventBitCondition(_BitCondition):
    @staticmethod
    def base_address():
        return event_bit.base_address()

    def write(self, bit, true = None, false = None):
        return super().write(event_bit.address(bit), event_bit.bit(bit), true, false)

class BattleBitCondition(_BitCondition):
    @staticmethod
    def base_address():
        return battle_bit.base_address()

    def write(self, bit, true = None, false = None):
        return super().write(battle_bit.address(bit), battle_bit.bit(bit), true, false)

class CharacterCondition(_BitCondition):
    @staticmethod
    def base_address():
        return event_bit.base_address()

    def write(self, character, true = None, false = None):
        return super().write(event_bit.address(event_bit.character_recruited(character)), character % 8, true, false)

class EsperCondition(_BitCondition):
    @staticmethod
    def base_address():
        return 0x1a69

    def write(self, esper, true = None, false = None):
        return super().write(EsperCondition.base_address() + esper // 8, esper % 8, true, false)

class EventWordCondition(_Condition):
    @staticmethod
    def base_address():
        return event_word.base_address() # add EVENT_WORD * 2 byte offset

    def write(self, word, count, ge = None, lt = None):
        if ge is None:
            ge = []
        if lt is None:
            lt = []

        src = [
            asm.LDA(event_word.address(word), asm.ABS),
            asm.CMP(count, asm.IMM8),
            asm.BLT("LT"),

            ge,
            asm.RTS(),

            "LT",
            lt,
            asm.RTS(),
        ]
        return Write(Bank.F0, src, f"battle word condition {hex(word)} {count}")
