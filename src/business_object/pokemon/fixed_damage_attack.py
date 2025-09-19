from business_object.pokemon.abstract_attack import AbstractAttack


class FixedDamageAttack(AbstractAttack):
    """
    Attack that does a fixed amount of damage, regardless of stats.
    """

    def compute_damage(self, attacker, defender) -> int:
        return self._power
