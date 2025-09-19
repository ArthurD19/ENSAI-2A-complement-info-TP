from typing import List, Optional
from dao.type_attack_dao import TypeAttackDAO
from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.attack.abstract_attack import AbstractAttack


class AttackDao(metaclass=Singleton):
    # ----------------------- ADD -----------------------
    def add_attack(self, attack: AbstractAttack) -> bool:
        """
        Add an attack to the database
        """
        created = False

        # Get the id type
        id_attack_type = TypeAttackDAO().find_id_by_label(attack.type)
        if id_attack_type is None:
            return created

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tp.attack
                        (id_attack_type, attack_name, power, accuracy, element, attack_description)
                    VALUES
                        (%(id_attack_type)s, %(name)s, %(power)s, %(accuracy)s, %(element)s, %(description)s)
                    RETURNING id_attack;
                    """,
                    {
                        "id_attack_type": id_attack_type,
                        "name": attack.name,
                        "power": attack.power,
                        "accuracy": attack.accuracy,
                        "element": attack.element,
                        "description": attack.description,
                    },
                )
                res = cursor.fetchone()
        if res:
            attack.id = res["id_attack"]
            created = True

        return created

    # ----------------------- FIND BY ID -----------------------
    def find_attack_by_id(self, id_attack: int) -> Optional[AbstractAttack]:
        """
        Find a single attack by its ID
        """
        from business_object.attack.attack_factory import AttackFactory

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT a.id_attack,
                           a.attack_name,
                           a.power,
                           a.accuracy,
                           a.element,
                           a.attack_description,
                           t.attack_type_name
                      FROM tp.attack a
                           JOIN tp.attack_type t
                             ON a.id_attack_type = t.id_attack_type
                     WHERE a.id_attack = %s;
                    """,
                    (id_attack,)
                )
                row = cursor.fetchone()

        if row:
            return AttackFactory().instantiate_attack(
                type=row["attack_type_name"],  
                id=row["id_attack"],
                power=row["power"],
                name=row["attack_name"],
                description=row["attack_description"],
                accuracy=row["accuracy"],
                element=row["element"],
            )
        return None

    # ----------------------- FIND ALL -----------------------
    def find_all_attacks(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[AbstractAttack]:
        """
        Return all attacks (with optional pagination)
        """
        from business_object.attack.attack_factory import AttackFactory

        query = """
            SELECT a.id_attack,
                   a.attack_name,
                   a.power,
                   a.accuracy,
                   a.element,
                   a.attack_description,
                   t.attack_type_name
              FROM tp.attack a
                   JOIN tp.attack_type t
                     ON a.id_attack_type = t.id_attack_type
             ORDER BY a.attack_name
        """
        params = {}
        if limit is not None:
            query += " LIMIT %(limit)s"
            params["limit"] = limit
        if offset is not None:
            query += " OFFSET %(offset)s"
            params["offset"] = offset

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()

        return [
            AttackFactory().instantiate_attack(
                type=row["attack_type_name"],  # DIRECT
                id=row["id_attack"],
                power=row["power"],
                name=row["attack_name"],
                description=row["attack_description"],
                accuracy=row["accuracy"],
                element=row["element"],
            )
            for row in rows
        ]

    # ----------------------- UPDATE -----------------------
    def update_attack(self, attack: AbstractAttack) -> bool:
        """
        Update an attack in the database
        """
        updated = False

        id_attack_type = TypeAttackDAO().find_id_by_label(attack.type)
        if id_attack_type is None:
            return updated

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tp.attack
                       SET id_attack_type = %(id_attack_type)s,
                           attack_name = %(name)s,
                           power = %(power)s,
                           accuracy = %(accuracy)s,
                           element = %(element)s,
                           attack_description = %(description)s
                     WHERE id_attack = %(id_attack)s;
                    """,
                    {
                        "id_attack_type": id_attack_type,
                        "name": attack.name,
                        "power": attack.power,
                        "accuracy": attack.accuracy,
                        "element": attack.element,
                        "description": attack.description,
                        "id_attack": attack.id,
                    },
                )
                if cursor.rowcount > 0:
                    updated = True

        return updated

