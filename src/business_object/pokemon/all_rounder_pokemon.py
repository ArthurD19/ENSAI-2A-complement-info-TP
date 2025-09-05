from business_object.pokemon.abstract_pokemon import AbstractPokemon


class AllRounderPokemon(AbstractPokemon):
    """
    All rounder Pokemon.
    """

    def __init__(self, stat_max=None, stat_current=None, level=0, name=None):
        super().__init__(stat_max, stat_current, level, name, type_pk="All rounder")

    def get_pokemon_attack_coef(self) -> float:
        return 1 + (self.sp_atk_current + self.sp_def_current) / 200
