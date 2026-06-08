import requests

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