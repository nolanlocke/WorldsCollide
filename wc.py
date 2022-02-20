def wc(args):
    import log

    from memory.memory import Memory
    memory = Memory()

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
    is_coop = True
    if is_coop:
        orig_seed = args.seed
        args.seed = f"{args.seed}-A"
        args.character_seed = f"{orig_seed}-Character"
        args.chest_seed = f"{orig_seed}-Chest"
        args.monster_seed = f"{orig_seed}-Monster"
        args.shop_seed = f"{orig_seed}-Shop"
        wc(args)
        args.seed = f"{args.seed}-B"
        wc(args)
    else:
        wc(args)

if __name__ == '__main__':
    main()
