from business_object.pokemon.attacker_pokemon import AttackerPokemon
from business_object.statistic import Statistic


class TestAttackerPokemon:
    def test_get_coef_damage_type(self):
        # GIVEN
        pikachu = AttackerPokemon(stat_current=Statistic(speed=150, attack=50))

        # WHEN
        multiplier = pikachu.get_pokemon_attack_coef()

        # THEN
        assert multiplier == 2


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
