import os
import pdb
import pandas as pd

from pathlib import Path
from pprint import pprint

class Pokemon:

    current_dir = Path(_file_).parent
    ### TODO: Move to another module     
    # If moved, uses import from that module
    csv_path = current_dir / "utils" / "First30Pokemons.csv"
    definition = """
    Pocket Monster
    """
    def _init_(
            self,
            pokemon_name: str,
            pokedex_num: int,
            type: str, 
            color: str,
            sex: str,
            level: int = 1
        ) -> None:
        """
        Creates a basic pokemon

        Args:
            name (int): Pokemon's name in lowercase
            pokedex_num (int): Number in the national pokedex
            type (str): Main type of the pokemon
        Returns:
           A string representation of the Pokemon.

        Raises:
            ...
        """
        #* Changed to protected so that subclasses can access them
        self._name = pokemon_name
        self._pokedex_num = pokedex_num
        self._main_type = type
        self._color = color
        self._sex = sex
        self._level = level if level >= 1 and level <= 100 else 1
        # Always creating base stats
        self._stats = Stats(
            csv_path=str(Pokemon.csv_path), 
            pokedex_num=pokedex_num,
            level=self._level # Level will affect base stats
        )
        # se agregó la última línea para que las estadísticas base se ajusten
        # al nivel del Pokémon
        #! Here logic can be added to modify stats based on level

        #* Changed to protected
        self._weaknesses = []
        self._resistances = []
        self._immunities = []

        ## TODO: Moveset
        # Shoudl be managed by another class -> composition
        # Because a pokemon HAS a moveset
        # This is a tricky one, moveset depends on level, type and pokemon
        # One approach is having a table with all moves and their characteristics
        # Then, based on level and type, assign a moveset to the pokemon
        # It implies join tables
        # Table: Moves | id | name | type | power | accuracy | pp |
        # Table: Pokemon_Moves | pokemon_id | move_id | level_learned |
        # So joining these tables and return all moves that the pokemon can learn
        # Then, select up to 4 moves based on level
        #! A pokemon can have up to 4 moves

    def level_up(self):
        #* Add docstring
        if self._level < 100:
            self._level += 1
            growth = 1.03 # 3% growth per level
            #* Alternatively, recalculate stats using the Stats class

            #? Check where these multipliers come from
            self._stats.hp = round(self._stats.hp * growth)
            self._stats.attack = round(self._stats.attack * growth)
            self._stats.defense = round(self._stats.defense * growth)
            self._stats.sp_attack = round(self._stats.sp_attack * growth)
            self._stats.sp_defense = round(self._stats.sp_defense * growth)
            self._stats.speed = round(self._stats.speed * growth)
            
            print(f"{self._name} leveled up to level {self._level}!")
        else:
            print(f"{self._name} is already max level!")

    def attack(self) -> str:
        ### TODO: Return necessary information to compute attack
        return f"{self._name} is attacking!"
    
    def receive_attack(self, attack_type):
        ### TODO: Return necessary information to compute damage
        if attack_type in self._immunities:
            return "It's inmune!"
        elif attack_type in self._weaknesses:
            return "It's super effective!"
        elif attack_type in self._resistances:
            return "It's not very effective..."
        else:
            return "It's effective."
        
    def update_stats_after_battle(self):
        ### TODO: Update stats based on battle outcomes
        pass

    def get_stats(self):
        return self._stats
    
    def get_attribute(self, attribute_name: str):
        # Dictionary mapping public names to protected attributes
        attribute_map = {
            'pokemon_name': self._name,  
            'pokedex_num': self._pokedex_num,
            'main_type': self._main_type,
            'type': self._main_type, 
            'color': self._color,
            'sex': self._sex,
            'level': self._level,
            'stats': self._stats,
            'weaknesses': self._weaknesses,
            'resistances': self._resistances,
            'immunities': self._immunities
        }
        
        if attribute_name in attribute_map:
            return attribute_map.get(attribute_name)
        else:
            raise AttributeError(f"Pokemon has no attribute '{attribute_name}'")
        
    def _str_(self):
        return (f"{self._name} (#{self._pokedex_num})"
                f"Type: {self._main_type}, Level: {self._level}")


### TODO: Move to another module      
class Stats():
    def _init_(self, csv_path: str, pokedex_num: int, level: int = 1):
        
        df = pd.read_csv(csv_path)
        row = df.loc[df['pokedex_number'] == pokedex_num]
        self.base_hp = int(row['hp'])
        self.base_attack = int(row['attack'])
        self.base_defense = int(row['defense'])
        self.base_sp_attack = int(row['sp_atk'])
        self.base_sp_defense = int(row['sp_def'])
        self.base_speed = int(row['speed'])

        #Linear growth factor: +3% for each additional level
        growth = 1 + (0.03 * (level - 1))

        self.base_hp = round(self.base_hp * growth)
        self.base_attack = round(self.base_attack * growth)
        self.base_defense = round(self.base_defense * growth)
        self.base_sp_attack = round(self.base_sp_attack * growth)
        self.base_sp_defense = round(self.base_sp_defense * growth)
        self.base_speed = round(self.base_speed * growth)



    def combat_stats(self, accuracy = "100%", evasion = "100%"):
        self.accuracy = accuracy
        self.evasion = evasion

    def _str_(self):
        return (
            f"HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}, "
            f"Sp. Attack: {self.sp_attack}, Sp. Defense: {self.sp_defense}, Speed: {self.speed}"
        )

class Normal(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Normal", color, sex, level)
        self._weaknesses = ["Fighting"]
        self._resistances = []
        self._immunities = ["Ghost"]

class Fire(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Fire", color, sex, level)
        self._weaknesses = ["Water", "Ground", "Rock"]
        self._resistances = ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"]
        self._immunities = []

class Water(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Water", color, sex, level)
        self._weaknesses = ["Electric", "Grass"]
        self._resistances = ["Fire", "Water", "Ice", "Steel"]
        self._immunities = []

class Grass(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Grass", color, sex, level)
        self._weaknesses = ["Fire", "Ice", "Poison", "Flying", "Bug"]
        self._resistances = ["Water", "Grass", "Electric", "Ground"]
        self._immunities = []

class Electric(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Electric", color, sex, level)
        self._weaknesses = ["Ground"]
        self._resistances = ["Electric", "Flying", "Steel"]
        self._immunities = []

class Ice(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Ice", color, sex, level)
        self._weaknesses = ["Fire", "Fighting", "Rock", "Steel"]
        self._resistances = ["Ice"]
        self._immunities = []

class Fighting(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Fighting", color, sex, level)
        self._weaknesses = ["Flying", "Psychic", "Fairy"]
        self._resistances = ["Bug", "Rock", "Dark"]
        self._immunities = []

class Poison(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Poison", color, sex, level)
        self._weaknesses = ["Ground", "Psychic"]
        self._resistances = ["Grass", "Fighting", "Poison", "Bug", "Fairy"]
        self._immunities = []

class Ground(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Ground", color, sex, level)
        self._weaknesses = ["Water", "Grass", "Ice"]
        self._resistances = ["Poison", "Rock"]
        self._immunities = ["Electric"]

class Flying(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Flying", color, sex, level)
        self._weaknesses = ["Electric", "Ice", "Rock"]
        self._resistances = ["Grass", "Fighting", "Bug"]
        self._immunities = ["Ground"]

class Psychic(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Psychic", color, sex, level)
        self._weaknesses = ["Bug", "Ghost", "Dark"]
        self._resistances = ["Fighting", "Psychic"]
        self._immunities = []

class Bug(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Bug", color, sex, level)
        self._weaknesses = ["Fire", "Flying", "Rock"]
        self._resistances = ["Grass", "Fighting", "Ground"]
        self._immunities = []

class Rock(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Rock", color, sex, level)
        self._weaknesses = ["Water", "Grass", "Fighting", "Ground", "Steel"]
        self._resistances = ["Normal", "Fire", "Poison", "Flying"]
        self._immunities = []

class Ghost(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Ghost", color, sex, level)
        self._weaknesses = ["Ghost", "Dark"]
        self._resistances = ["Poison", "Bug"]
        self._immunities = ["Normal", "Fighting"]

class Dragon(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Dragon", color, sex, level)
        self._weaknesses = ["Ice", "Dragon", "Fairy"]
        self._resistances = ["Fire", "Water", "Grass", "Electric"]
        self._immunities = []

class Dark(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Dark", color, sex, level)
        self._weaknesses = ["Fighting", "Bug", "Fairy"]
        self._resistances = ["Ghost", "Dark"]
        self._immunities = ["Psychic"]

class Steel(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Steel", color, sex, level)
        self._weaknesses = ["Fire", "Fighting", "Ground"]
        self._resistances = [
            "Normal", "Grass", "Ice", "Flying", "Psychic", "Bug",
            "Rock", "Dragon", "Steel", "Fairy"
        ]
        self._immunities = ["Poison"]

class Fairy(Pokemon):
    def _init_(self, name, pokedex_num, color, sex, level=1):
        super()._init_(name, pokedex_num, "Fairy", color, sex, level)
        self._weaknesses = ["Poison", "Steel"]
        self._resistances = ["Fighting", "Bug", "Dark"]
        self._immunities = ["Dragon"]

if _name_ == "_main_":
    bulbasaur = Pokemon(
        "bulbasaur",
        1,
        "grass",
        "blue",
        "male"
    )
    print(bulbasaur)
    bulbasaur.attack()
    print(bulbasaur.get_stats())
    charmander = Pokemon(
        "charmander",
        4,
        "fire",
        "orange",
        "male"
    )
    charmander.attack()
    print(charmander.get_stats())
