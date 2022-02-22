from memory.rom import ROM
from memory.space import Space
from memory.free import free

class Memory:
    def __init__(self, args):
        self.args = args
        self.rom = ROM(self.args.input_file)

    # must be called after space has been reset.
    def free(self):
        free()

    def write(self):
        if not self.args.no_rom_output:
            self.rom.write(f"{self.args.output_file}{self.args.output_file_ext}")
