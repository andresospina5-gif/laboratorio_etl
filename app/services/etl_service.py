import requests
from app.database import cartas_collection

def obtener_cartas(cantidad):

    cartas = []

    page = 1
    page_size = 250

    while len(cartas) < cantidad:

        response = requests.get(
            "https://api.pokemontcg.io/v2/cards",
            params={
                "page": page,
                "pageSize": page_size
            }
        )

        if response.status_code != 200:
            break

        data = response.json()["data"]

        if not data:
            break

        cartas.extend(data)

        page += 1

    return cartas[:cantidad]

def guardar_cartas_mongo(cartas):

    insertadas = 0

    for carta in cartas:

        carta["_id"] = carta["id"]

        resultado = cartas_collection.update_one(
            {"_id": carta["_id"]},
            {"$set": carta},
            upsert=True
        )

        if resultado.upserted_id:
            insertadas += 1

    return insertadas