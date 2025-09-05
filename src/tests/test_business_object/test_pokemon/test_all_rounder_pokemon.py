from business_object.pokemon.all_rounder_pokemon import AllRounderPokemon
from business_object.statistic import Statistic


class TestAllRounderPokemon:
    def test_get_coef_damage_type(self):
        # GIVEN
        lucario = AllRounderPokemon(stat_current=Statistic(sp_atk=90, sp_def=90))

        # WHEN
        multiplier = lucario.get_pokemon_attack_coef()

        # THEN
        assert multiplier == 1.9


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
