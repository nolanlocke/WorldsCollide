import random
from data.character import Character
from data.items import Items
from data.natural_magic import NaturalMagic
from data.commands import Commands
from data.menu_character_sprites import MenuCharacterSprites
from data.character_sprites import CharacterSprites
from data.character_palettes import CharacterPalettes
from data.party_battle_scripts import PartyBattleScripts
from data.structures import DataArray

import data.characters_asm as characters_asm
from memory.rom import ROM

class Characters():
    CHARACTER_COUNT = 14   # 14 playable characters
    TERRA, LOCKE, CYAN, SHADOW, EDGAR, SABIN, CELES, STRAGO, RELM, SETZER, MOG, GAU, GOGO, UMARO = range(CHARACTER_COUNT)
    SOLDIER, IMP, GENERAL_LEO, BANON_DUNCAN, ESPER_TERRA, MERCHANT, GHOST, KEFKA = range(CHARACTER_COUNT, 22)

    # The ID's above are actually the sprite IDs rather than the character ids
    BANON = 14
    LEO = 15

    DEFAULT_POOL = ["TERRA", "LOCKE", "CYAN", "SHADOW", "EDGAR", "SABIN", "CELES", "STRAGO", "RELM", "SETZER", "MOG", "GAU", "GOGO", "UMARO", "BANON", "LEO"]
    DEFAULT_NAME = ["TERRA", "LOCKE", "CYAN", "SHADOW", "EDGAR", "SABIN", "CELES", "STRAGO", "RELM", "SETZER", "MOG", "GAU", "GOGO", "UMARO"]

    INIT_DATA_START = 0x2d7ca0
    INIT_DATA_END = 0x2d821f
    INIT_DATA_SIZE = 22

    NAMES_START = 0x478c0
    NAMES_END = 0x47a3f
    NAME_SIZE = 6

    def __init__(self, rom: ROM, args, spells):
        from data.item_names import name_id
        from constants.commands import name_id
        self.rom = rom
        self.args = args

        self.init_data = DataArray(self.rom, self.INIT_DATA_START, self.INIT_DATA_END + self.INIT_DATA_SIZE * 2, self.INIT_DATA_SIZE)
        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END + self.NAME_SIZE * 2, self.NAME_SIZE)

        self.characters = []
        banon_target_index = 1 # args.banon_id
        leo_target_index = 3 # args.leo_id
        for character_index in range(len(self.name_data)):
            source_idx = Characters.LEO if character_index == leo_target_index else Characters.BANON if character_index == banon_target_index else character_index
            character = Character(character_index, self.init_data[source_idx], self.name_data[source_idx])
            if source_idx == Characters.LEO or source_idx == Characters.BANON:
                character.commands[0] = name_id["Fight"] # overwrite fight in case we replace gau
                character.commands[2] = name_id["Magic"] # add magic command to equip espers
                character.init_relic2 = Items.EMPTY # Leo starts with an Offering in this slot
            if source_idx == Characters.LEO:
                character.init_vigor = 40 # orig 52
                character.init_magic = 28 # orig 36
                character.init_evasion = 25 # orig 22
                character.init_magic_evasion = 25 # orig 21
            if source_idx == Characters.BANON:
                character.init_magic = 35 # orig 32
                character.init_evasion = 20 # orig 36
                character.init_magic_evasion = 20 # orig 32
            self.characters.append(character)

        self.playable = self.characters[:self.CHARACTER_COUNT]

        self.natural_magic = NaturalMagic(self.rom, self.args, self, spells)
        self.commands = Commands(self.characters)

        self.menu_character_sprites = MenuCharacterSprites(self.rom, self.args)
        self.character_sprites = CharacterSprites(self.rom, self.args)
        self.character_palettes = CharacterPalettes(self.rom, self.args, self.menu_character_sprites)

        self.battle_scripts = PartyBattleScripts(self.rom, self.args, self)

        self.available_characters = list(range(len(self.DEFAULT_NAME)))

        # path of characters required to unlock each character
        # e.g. self.character_paths[self.TERRA] = all characters required for terra (in order)
        self.character_paths = [[] for char_index in range(len(self.DEFAULT_NAME))]

    def get_available_count(self):
        return len(self.available_characters)

    def set_unavailable(self, character):
        self.available_characters.remove(character)

    def get_random_available(self, exclude = None):
        if exclude is None:
            exclude = []

        import random
        possible_characters = [character_id for character_id in self.available_characters if character_id not in exclude]
        random_character = random.choice(possible_characters)
        self.set_unavailable(random_character)
        return random_character

    def set_character_path(self, character, required_character):
        if required_character is not None:
            self.character_paths[character].extend(self.character_paths[required_character])
            self.character_paths[character].append(required_character)

    def get_character_path(self, character):
        return self.character_paths[character]

    def mod_init_levels(self):
        if self.args.start_average_level:
            # characters recruited at average level, set everyone's initial level to 3
            for character in self.characters:
                character.init_level_factor = 0

    def stats_random_percent(self):
        import random
        stats = ["init_extra_hp", "init_extra_mp", "init_vigor", "init_speed", "init_stamina", "init_magic",
                 "init_attack", "init_defense", "init_magic_defense", "init_evasion", "init_magic_evasion"]
        for character in self.characters:
            for stat in stats:
                stat_value = getattr(character, stat)
                if stat_value != 0:
                    character_stat_percent = random.randint(self.args.character_stat_random_percent_min,
                                                            self.args.character_stat_random_percent_max) / 100.0
                    value = int(stat_value * character_stat_percent)
                    setattr(character, stat, max(min(value, 255), 0))

    def get_characters_with_command(self, command_name):
        from constants.commands import name_id
        command_id = name_id[command_name]

        result = []
        for character in self.characters:
            if command_id in character.commands and character.id < 14:
                result.append(character.id)
        return result

    def mod_names(self):
        for character_id, name in enumerate(self.args.names):
            self.characters[character_id].name = name

    def mod_banon(self, exclude = []):
        self.mod_guest_into_game(self.BANON, self.LOCKE, [])

    def mod_leo(self):
        self.mod_guest_into_game(self.LEO, self.SHADOW, [self.BANON])

    def mod_guest_into_game(self, source_id, target_id, exclude = []):
        # Copy guest character's stats another character's
        import random
        from data.characters import Characters
        sacrifice = self.characters[target_id] # dont replace gau/gogo/umaro, they do weird things with skills
        source = self.characters[source_id]

        self.characters[target_id] = source
        self.characters[source_id] = sacrifice
        source.id = target_id
        sacrifice.id = source_id

    def mod(self):
        if self.args.start_naked:
            for char in self.characters:
                char.clear_init_equip()

        if self.args.equipable_umaro:
            characters_asm.equipable_umaro(self.CHARACTER_COUNT)

        self.mod_init_levels()

        if self.args.character_stat_random_percent:
            self.stats_random_percent()

        self.commands.mod()

        if self.args.character_names:
            self.mod_names()

        if self.args.original_name_display:
            characters_asm.show_original_names()

        # self.mod_banon()
        self.mod_leo()

        self.natural_magic.mod()
        self.character_sprites.mod()
        self.character_palettes.mod()
        self.battle_scripts.mod()

    def write(self):
        if self.args.spoiler_log:
            self.commands.log()

        for character_index in range(len(self.characters)):
            self.init_data[character_index] = self.characters[character_index].init_data()
            if character_index == 1:
                self.name_data[character_index] = self.characters[14].name_data()
            else:
                self.name_data[character_index] = self.characters[character_index].name_data()

        self.init_data.write()
        self.name_data.write()

        self.natural_magic.write()

        self.menu_character_sprites.write()
        self.character_sprites.write()
        self.character_palettes.write()
        self.battle_scripts.write()

    def print_character_paths(self):
        for char_index in range(self.CHARACTER_COUNT):
            path = self.get_character_path(char_index)
            for req_char_index in path:
                print(f"{self.DEFAULT_NAME[req_char_index]} -> ", end = '')
            print(f"{self.DEFAULT_NAME[char_index]}")

    def print(self):
        for char in self.characters:
            char.print()

    def get(self, character):
        for char in self.characters:
            if char.id == character:
                return char

    def get_by_name(self, name):
        for char in self.characters:
            if self.DEFAULT_NAME[char.id].lower() == name.lower():
                return char

    def get_name(self, character):
        return self.characters[character].name.rstrip('\0')

    def get_default_name(self, character):
        return self.DEFAULT_NAME[character]

    def get_sprite(self, character):
        return self.characters[character].sprite

    def get_random_esper_item_sprite(self):
        sprites = [self.SOLDIER, self.IMP, self.MERCHANT, self.GHOST]

        import random
        return sprites[random.randrange(len(sprites))]

    def get_palette(self, character):
        return self.character_palettes.get(character)
