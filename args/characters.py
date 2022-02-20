def name():
    return "Characters"

def parse(parser):
    characters = parser.add_argument_group("Characters")

    # from data.characters import Characters
    # # choosing to ignore these three due to odd skills
    # ignore_characters = [
    #     Characters.DEFAULT_NAME[Characters.MOG],
    #     Characters.DEFAULT_NAME[Characters.GOGO],
    #     Characters.DEFAULT_NAME[Characters.UMARO]
    # ]
    # character_options = [name.lower() for name in Characters.DEFAULT_NAME if name not in ignore_characters]
    # character_options.append("random")

    characters.add_argument("-sal", "--start-average-level", action = "store_true",
                            help = "Recruited characters start at the average character level")
    characters.add_argument("-sn", "--start-naked", action = "store_true",
                            help = "Recruited characters start with no equipment")
    characters.add_argument("-eu", "--equipable-umaro", action = "store_true",
                            help = "Umaro can access equipment menu")
    characters.add_argument("-csrp", "--character-stat-random-percent", default = [100, 100], type = int,
                            nargs = 2, metavar = ("MIN", "MAX"), choices = range(201),
                            help = "Each character stat set to random percent of original within given range ")
    # characters.add_argument("-banon", "--banon-is", default = "", type = str.lower, choices = character_options,
    #                         help = "Banon replaces target character, making that character's checks ungated")

def process(args):
    args._process_min_max("character_stat_random_percent")

def flags(args):
    flags = ""

    if args.start_average_level:
        flags += " -sal"
    if args.start_naked:
        flags += " -sn"
    if args.equipable_umaro:
        flags += " -eu"
    # if args.banon_is:
    #     flags += f" -banon {args.banon_is}"
    if args.character_stat_random_percent_min != 100 or args.character_stat_random_percent_max != 100:
        flags += f" -csrp {args.character_stat_random_percent_min} {args.character_stat_random_percent_max}"

    return flags

def options(args):
    character_stats = f"{args.character_stat_random_percent_min}-{args.character_stat_random_percent_max}%"
    from data.characters import Characters
    banon_is_name = Characters.DEFAULT_NAME if True else None
    return [
        ("Start Average Level", args.start_average_level),
        ("Start Naked", args.start_naked),
        ("Equipable Umaro", args.equipable_umaro),
        ("Character Stats", character_stats),
        ("Banon Is", [name.lower() for name in Characters.DEFAULT_NAME]
),
    ]

def menu(args):
    entries = options(args)
    for index, entry in enumerate(entries):
        key, value = entry
        if key == "Character Stats":
            entries[index] = ("Stats", entry[1])
    return (name(), entries)

def log(args):
    from log import format_option
    log = [name()]

    entries = options(args)
    for entry in entries:
        log.append(format_option(*entry))

    return log
