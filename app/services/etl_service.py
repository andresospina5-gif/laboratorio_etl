import requests

def obtener_cartas(cantidad):

    url = "https://api.pokemontcg.io/v2/cards"

    response = requests.get(
        url,
        params={
            "page": 1,
            "pageSize": cantidad
        }
    )

    if response.status_code != 200:
        return []

    data = response.json()

    return data["data"]