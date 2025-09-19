from dao.attack_dao import AttackDao
import random


class TestAttackDao:
    def test_find_attack_by_id_ok(self):
        # GIVEN
        existing_id_attack = 1

        # WHEN
        attack = AttackDao().find_attack_by_id(existing_id_attack)

        # THEN
        assert attack is not None
        assert attack.id == existing_id_attack

    def test_add_attack(self):
        # GIVEN
        from business_object.attack.physical_attack import PhysicalFormulaAttack
        attack = PhysicalFormulaAttack(
            power=50,
            name=f"TestAttack_{random.randint(1, 10000)}",  # nom unique
            description="Test Description2",
            accuracy=100,
            element="Normal",
        )

        # WHEN
        result = AttackDao().add_attack(attack)

        # THEN
        assert result is True
        assert attack.id is not None  

    def test_update_attack(self):
        # GIVEN
        dao = AttackDao()
        attack = dao.find_attack_by_id(1)
        original_name = attack.name
        attack.name = "UpdatedAttack"

        # WHEN
        result = dao.update_attack(attack)

        # THEN
        assert result is True
        updated_attack = dao.find_attack_by_id(1)
        assert updated_attack.name == "UpdatedAttack"

        # Reset (optional)
        attack.name = original_name
        dao.update_attack(attack)
