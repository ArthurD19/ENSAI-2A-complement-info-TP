from business_object.pokemon.abstract_formula_attack import AbstractFormulaAttack


class PhysicalFormulaAttack(AbstractFormulaAttack):
    """
    Physical attacks use the attack stat of the attacker and defense stat of the defender.
    """

    def get_attack_stat(self, attacker) -> float:
        return attacker.attack_current

    def get_defense_stat(self, defender) -> float:
        return defender.defense_current
