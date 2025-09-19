from business_object.pokemon.abstract_formula_attack import AbstractFormulaAttack


class SpecialFormulaAttack(AbstractFormulaAttack):
    """
    Special attacks use the special attack of the attacker and special defense of the defender.
    """

    def get_attack_stat(self, attacker) -> float:
        return attacker.sp_atk_current

    def get_defense_stat(self, defender) -> float:
        return defender.sp_def_current
