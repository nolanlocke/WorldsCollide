from memory.space import Bank, Reserve, Write, Read
import instruction.asm as asm
import args

class ScanAll:
    def __init__(self):
        if args.scan_all:
            self.teach_scan()

    def teach_scan(self):
        None #noop