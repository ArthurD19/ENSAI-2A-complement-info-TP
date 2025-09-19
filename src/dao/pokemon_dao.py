from typing import List, Optional
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from business_object.pokemon.abstract_pokemon import AbstractPokemon
from business_object.pokemon.pokemon_factory import PokemonFactory
from dao.attack_dao import AttackDao


class PokemonDAO(metaclass=Singleton):
    # ----------------------- FIND BY NAME -----------------------
    def find_pokemon_by_name(self, name: str) -> Optional[AbstractPokemon]:
        """
        Find a single Pokémon by its name
        """
        query = """
            SELECT p.id_pokemon,
                   p.name,
                   t.pokemon_type_name
              FROM tp.pokemon p
                   JOIN tp.pokemon_type t
                     ON p.id_pokemon_type = t.id_pokemon_type
             WHERE p.name = %s;
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (name,))
                row = cursor.fetchone()

        if row:
            # Create Pokémon object via the factory
            pokemon = PokemonFactory().instantiate_pokemon(
                id=row["id_pokemon"],
                name=row["name"],
                type=row["pokemon_type_name"]
            )

            # Retrieve attacks for this Pokémon
            attacks_query = """
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
                       JOIN tp.pokemon_attack pa
                         ON pa.id_attack = a.id_attack
                 WHERE pa.id_pokemon = %s
                 ORDER BY a.attack_name;
            """
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(attacks_query, (row["id_pokemon"],))
                    attack_rows = cursor.fetchall()

            pokemon.attacks = [
                AttackDao().find_attack_by_id(a["id_attack"]) for a in attack_rows
            ]

            return pokemon

        return None

    # ----------------------- FIND ALL -----------------------
    def find_all_pokemon(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[AbstractPokemon]:
        """
        Return all Pokémon (with optional pagination)
        """
        query = """
            SELECT p.id_pokemon,
                   p.name,
                   t.pokemon_type_name
              FROM tp.pokemon p
                   JOIN tp.pokemon_type t
                     ON p.id_pokemon_type = t.id_pokemon_type
             ORDER BY p.name
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

        pokemons = []
        for row in rows:
            pokemon = PokemonFactory().instantiate_pokemon(
                id=row["id_pokemon"],
                name=row["name"],
                type=row["pokemon_type_name"]
            )

            # Retrieve attacks for each Pokémon
            attacks_query = """
                SELECT a.id_attack
                  FROM tp.attack a
                       JOIN tp.pokemon_attack pa
                         ON pa.id_attack = a.id_attack
                 WHERE pa.id_pokemon = %s;
            """
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(attacks_query, (row["id_pokemon"],))
                    attack_rows = cursor.fetchall()

            pokemon.attacks = [
                AttackDao().find_attack_by_id(a["id_attack"]) for a in attack_rows
            ]

            pokemons.append(pokemon)

        return pokemons
