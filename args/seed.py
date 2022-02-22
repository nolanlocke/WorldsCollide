def name():
    return "seed"

def parse(parser):
    seed_spoilers = parser.add_argument_group("Targeted Seeds")
    # seed_spoilers.add_argument("-scheck", dest = "check_seed", type = str, required = False, help = "RNG Seed for check shuffling")
    seed_spoilers.add_argument("-schar", dest = "character_seed", type = str, required = False, help = "RNG Seed for starting characters, abilities and stats")
    seed_spoilers.add_argument("-schest", dest = "chest_seed", type = str, required = False, help = "RNG Seed for chest shuffling and item randomization")
    seed_spoilers.add_argument("-senemy", dest = "enemy_seed", type = str, required = False, help = "RNG Seed for enemy and boss shuffling")
    seed_spoilers.add_argument("-sshop", dest = "shop_seed", type = str, required = False, help = "RNG Seed for shop shuffling")

def process(args):
    pass

def flags(args):
    flags = ""

    if args.character_seed:
        flags += f" -schar {args.seed}-{args.character_seed}"
    else:
        flags += f" -schar {args.seed}"

    if args.chest_seed:
        flags += f" -schest {args.seed}-{args.chest_seed}"
    else:
        flags += f" -schar {args.seed}"

    if args.enemy_seed:
        flags += f" -senemy {args.seed}-{args.enemy_seed}"
    else:
        flags += f" -schar {args.seed}"

    if args.shop_seed:
        flags += f" -sshop {args.seed}-{args.shop_seed}"
    else:
        flags += f" -schar {args.seed}"

    return flags

def options(args):
    return []

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        if entry[0] == "Seed":
            if len(entry[1]) > 18:
                entries[index] = (entry[0], entry[1][:15] + "...")
            break
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
