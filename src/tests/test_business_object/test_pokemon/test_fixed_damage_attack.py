from business_object.pokemon.fixed_damage_attack import FixedDamageAttack
from business_object.pokemon.attacker_pokemon import AttackerPokemon
from business_object.statistic import Statistic


class TestFixedDamageAttack:
    def test_fixed_damage(self):
        # GIVEN
        stats = Statistic(attack=50, defense=40, sp_atk=30, sp_def=20, speed=60, hp=100)
        attacker = AttackerPokemon(stat_max=stats, stat_current=stats, level=5, name="Pikachu")
        attack = FixedDamageAttack(name="Tackle", power=35)

        # WHEN
        damage = attack.compute_damage(attacker, attacker)

        # THEN
        assert damage == 35


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
