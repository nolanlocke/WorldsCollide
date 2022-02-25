def name():
    return "seed"

def parse(parser):
    seed_spoilers = parser.add_argument_group("Subseed")
    seed_spoilers.add_argument("-scheck", dest = "subseed_check", type = str, required = False, help = "RNG Seed for check shuffling (A secondary shuffle after starting characters have been determined)")
    seed_spoilers.add_argument("-sstart", dest = "subseed_start", type = str, required = False, help = "RNG Seed for starting characters and stats")
    seed_spoilers.add_argument("-scommand", dest = "subseed_command", type = str, required = False, help = "RNG Seed for commands")
    seed_spoilers.add_argument("-schest", dest = "subseed_chest", type = str, required = False, help = "RNG Seed for chest shuffling and item randomization")
    seed_spoilers.add_argument("-snormal", dest = "subseed_normal", type = str, required = False, help = "RNG Seed for normal enemy shuffling, coliseum enemies")
    seed_spoilers.add_argument("-sboss", dest = "subseed_boss", type = str, required = False, help = "RNG Seed for boss boss shuffling")
    seed_spoilers.add_argument("-sshop", dest = "subseed_shop", type = str, required = False, help = "RNG Seed for shop shuffling")
    seed_spoilers.add_argument("-sesper", dest = "subseed_esper", type = str, required = False, help = "RNG Seed for esper shuffling, bonuses, and spells")
    seed_spoilers.add_argument("-scoli", dest = "subseed_coliseum", type = str, required = False, help = "RNG Seed for coliseum shuffling, including both monsters and items")
    seed_spoilers.add_argument("-sauction", dest = "subseed_auction_house", type = str, required = False, help = "RNG Seed for shuffling auction house items")

def process(args):
    pass

def flags(args):

    flags = ""

    return flags

def options(args):
    return []

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
