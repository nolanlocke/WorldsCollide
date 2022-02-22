
def wc(memory, args):
    import log


    from data.data import Data
    data = Data(memory.rom, args)

    from event.events import Events
    events = Events(memory.rom, args, data)

    from menus.menus import Menus
    menus = Menus(data.characters, data.dances)

    from battle import Battle
    battle = Battle()

    from settings import Settings
    settings = Settings()

    from bug_fixes import BugFixes
    bug_fixes = BugFixes()

    data.write()
    memory.write()

def main():
    import args
    from memory.memory import Memory
    from memory.space import Space

    # create memory instance
    memory = Memory(args)
    Space.initialize_space(memory.rom)
    memory.free()

    output_file = args.output_file

    orig_seed = args.seed
    args.output_file = f"{args.output_file}"
    wc(memory, args)

if __name__ == '__main__':
    main()
