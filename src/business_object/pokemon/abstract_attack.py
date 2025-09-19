from abc import ABC, abstractmethod


class AbstractAttack(ABC):
    """
    Abstract class for all attacks.
    """

    def __init__(self, name: str, power: int, description: str = ""):
        self._name = name
        self._power = power
        self._description = description

    @abstractmethod
    def compute_damage(self, attacker, defender) -> int:
        """
        Compute the damage inflicted on the defender by the attacker.
        Must be implemented in child classes.
        """
        pass

    @property
    def name(self):
        return self._name

    @property
    def power(self):
        return self._power

    @property
    def description(self):
        return self._description
