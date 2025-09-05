from abc import ABC, abstractmethod
import random
from business_object.pokemon.abstract_attack import AbstractAttack


class AbstractFormulaAttack(AbstractAttack, ABC):
    """
    Template class for variable damage attacks.
    """

    def compute_damage(self, attacker, defender) -> int:
        """
        Computes the damage using the formula:
        damage = power * (attack_stat / defense_stat) * random_multiplier
        """
        attack_stat = self.get_attack_stat(attacker)
        defense_stat = self.get_defense_stat(defender)
        random_multiplier = random.uniform(0.85, 1.0)

        damage = self._power * (attack_stat / defense_stat) * random_multiplier
        return max(1, int(damage))  # at least 1 damage

    @abstractmethod
    def get_attack_stat(self, attacker) -> float:
        """Return the relevant attack stat of the attacker."""
        pass

    @abstractmethod
    def get_defense_stat(self, defender) -> float:
        """Return the relevant defense stat of the defender."""
        pass
