from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional

from dao.attack_dao import AttackDao
from dao.pokemon_dao import PokemonDAO

app = FastAPI()


# ---------------------- HELLO ----------------------
@app.get("/hello")
async def get_hello():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def get_hello_name(name: str):
    return {"message": f"Hello {name}"}


# ---------------------- CHARACTERS ----------------------
class Personnage(BaseModel):
    nom: str
    age: int


characters_db: Dict[int, Personnage] = {}
characters_db[1] = Personnage(nom="Anne", age=33)
characters_db[2] = Personnage(nom="Michel", age=20)
character_id = 3


@app.get("/character/")
def list_characters():
    return characters_db


@app.post("/character/")
def create_character(character: Personnage):
    global character_id
    characters_db[character_id] = character
    character_id += 1
    return character


@app.put("/character/{character_id}")
def update_character(character_id: int, character: Personnage):
    if character_id not in characters_db:
        raise HTTPException(status_code=404, detail="Character not found")
    characters_db[character_id] = character
    return character


@app.delete("/character/{character_id}")
def delete_character(character_id: int):
    if character_id not in characters_db:
        raise HTTPException(status_code=404, detail="Character not found")
    deleted_character = characters_db.pop(character_id)
    return deleted_character


# ---------------------- POKEMON / ATTACK MODELS ----------------------
class AttackModel(BaseModel):
    id: int
    name: str
    type: str
    power: Optional[int]
    accuracy: Optional[int]
    element: Optional[str]
    description: Optional[str]


class PokemonModel(BaseModel):
    id: int
    name: str
    type: str
    attacks: List[AttackModel] = []


# ---------------------- ATTACK ENDPOINTS ----------------------
@app.get("/attack/", response_model=List[AttackModel])
async def get_all_attacks(limit: int = Query(100, description="Maximum number of attacks to return")):
    attacks = AttackDao().find_all_attacks(limit=limit)
    return [
        AttackModel(
            id=a.id,
            name=a.name,
            type=a.type,
            power=a.power,
            accuracy=a.accuracy,
            element=a.element,
            description=a.description
        ) for a in attacks
    ]


# ---------------------- POKEMON ENDPOINTS ----------------------
@app.get("/pokemon/", response_model=List[PokemonModel])
async def get_all_pokemons(limit: int = Query(100, description="Maximum number of Pokemons to return")):
    pokemons = PokemonDAO().find_all_pokemon()[:limit]
    result = []
    for p in pokemons:
        attacks = [
            AttackModel(
                id=a.id,
                name=a.name,
                type=a.type,
                power=a.power,
                accuracy=a.accuracy,
                element=a.element,
                description=a.description
            )
            for a in p.attacks
        ]
        result.append(PokemonModel(id=p.id, name=p.name, type=p.type, attacks=attacks))
    return result


@app.get("/pokemon/{name}", response_model=PokemonModel)
async def get_pokemon_by_name(name: str):
    p = PokemonDAO().find_pokemon_by_name(name)
    if not p:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    attacks = [
        AttackModel(
            id=a.id,
            name=a.name,
            type=a.type,
            power=a.power,
            accuracy=a.accuracy,
            element=a.element,
            description=a.description
        )
        for a in p.attacks
    ]
    return PokemonModel(id=p.id, name=p.name, type=p.pokemon_type, attacks=attacks)


# ---------------------- RUN APP ----------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
