from abc import ABC, abstractmethod
import random
from business_object.pokemon.abstract_attack import AbstractAttack


class AbstractFormulaAttack(AbstractAttack, ABC):
    """
    Template class for variable damage attacks.
    """

    def compute_damage(self, attacker, defender) -> int:
        """
        Computes the damage using the formula
        """
        level = attacker.level
        attack_stat = self.get_attack_stat(attacker)
        defense_stat = self.get_defense_stat(defender)
        random_multiplier = random.uniform(0.85, 1.0)

        damage = (((2 * level / 5 + 2) *
                  self._power * attack_stat / (defense_stat * 50)) + 2) * random_multiplier
        return int(damage)

    @abstractmethod
    def get_attack_stat(self, attacker) -> float:
        """Return the relevant attack stat of the attacker."""
        pass

    @abstractmethod
    def get_defense_stat(self, defender) -> float:
        """Return the relevant defense stat of the defender."""
        pass
