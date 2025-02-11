from memory.space import Bank, START_ADDRESS_SNES, Reserve, Allocate, Write
import instruction.asm as asm
import instruction.f0 as f0
import args

class CheckDragonBoss(asm.JSL):
    def __init__(self):
        # after battle check if boss/dragon was defeated, if so increment/set boss/dragon count/bit

        import data.event_word as event_word
        dragons_defeated_address = event_word.address(event_word.DRAGONS_DEFEATED)
        bosses_defeated_address = event_word.address(event_word.BOSSES_DEFEATED)

        import data.battle_bit as battle_bit
        boss_bits_start = battle_bit.address(battle_bit.BOSS_DEFEATED_START)
        dragon_bits_start = battle_bit.address(battle_bit.DRAGON_DEFEATED_START)

        src = [
            asm.PHP(),
            asm.AXY16(),

            asm.LDA(0x11e4, asm.ABS),               # a = veldt flag bits
            asm.BIT(0x0002, asm.IMM16),             # on veldt?
            asm.BNE("RETURN"),                      # if so, skip checking bosses/dragons

            "CHECK_DRAGON_FORMATIONS",
            asm.LDA(0x3ed4, asm.ABS),               # a = enemy formation
            asm.LDX(0x0000, asm.IMM16),             # formation table index = 0

            "DRAGON_CHECK_LOOP_START",
            asm.CMP(f0.dragon_formations, asm.LNG_X),
            asm.BEQ("INCREMENT_DRAGON_COUNT"),      # branch if formation in dragon formations
            asm.INX(),
            asm.INX(),
            asm.CPX(f0.dragon_formations_size, asm.IMM16),
            asm.BLT("DRAGON_CHECK_LOOP_START"),     # branch if not checked all dragon formations
            asm.BRA("CHECK_BOSS_FORMATIONS"),

            "INCREMENT_DRAGON_COUNT",
            asm.INC(dragons_defeated_address, asm.ABS),
            asm.TXA(),                              # a = formation index * 2
            asm.LSR(),                              # a = formation index
            asm.CLC(),
            asm.ADC(battle_bit.bit(battle_bit.DRAGON_DEFEATED_START), asm.IMM16),
            asm.LDX(0x0008, asm.IMM16),
            asm.JSR(f0.divide, asm.ABS),            # a = byte, x = bit
            asm.PHY(),
            asm.TAY(),                              # y = dragon battle byte
            asm.JSR(f0.set_bit_x, asm.ABS),         # set bit #x in a
            asm.ORA(dragon_bits_start, asm.ABS_Y),
            asm.STA(dragon_bits_start, asm.ABS_Y),  # set dragon defeated battle bit
            asm.PLY(),
            asm.BRA("RETURN"),

            "CHECK_BOSS_FORMATIONS",
            asm.LDX(0x0000, asm.IMM16),             # formation table index = 0

            "BOSS_CHECK_LOOP_START",
            asm.CMP(f0.boss_formations, asm.LNG_X),
            asm.BEQ("INCREMENT_BOSS_COUNT"),        # branch if formation in boss formations
            asm.INX(),
            asm.INX(),
            asm.CPX(f0.boss_formations_size, asm.IMM16),
            asm.BLT("BOSS_CHECK_LOOP_START"),       # branch if not checked all boss formations
            asm.BRA("RETURN"),

            "INCREMENT_BOSS_COUNT",
            asm.INC(bosses_defeated_address, asm.ABS),
            asm.TXA(),                              # a = formation index * 2
            asm.LSR(),                              # a = formation index
            asm.CLC(),
            asm.ADC(battle_bit.bit(battle_bit.BOSS_DEFEATED_START), asm.IMM16),
            asm.LDX(0x0008, asm.IMM16),
            asm.JSR(f0.divide, asm.ABS),            # a = byte, x = bit
            asm.PHY(),
            asm.TAY(),                              # y = boss battle byte
            asm.JSR(f0.set_bit_x, asm.ABS),         # set bit #x in a
            asm.ORA(boss_bits_start, asm.ABS_Y),
            asm.STA(boss_bits_start, asm.ABS_Y),    # set boss defeated battle bit
            asm.PLY(),

            "RETURN",
            asm.PLP(),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "update boss/dragon count/bit")
        CheckDragonBoss.__init__ = lambda self : super().__init__(START_ADDRESS_SNES + space.start_address)
        self.__init__()
